package com.brookes.ve_calais_obd2

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothSocket
import android.content.Context
import kotlinx.coroutines.*
import timber.log.Timber
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.util.*

class BluetoothManager(private val context: Context) {

    private var bluetoothSocket: BluetoothSocket? = null
    private var inputReader: BufferedReader? = null
    private var outputWriter: OutputStreamWriter? = null
    private var connectionJob: Job? = null
    private val scope = CoroutineScope(Dispatchers.IO + Job())

    var isConnected = false
        private set

    var connectionCallback: ((isConnected: Boolean, error: String?) -> Unit)? = null
    var dataCallback: ((data: String) -> Unit)? = null

    // Sniffer hook: when set, every command sent and response received is reported here too,
    // regardless of AppPreferences.isSnifferEnabled - callers (SnifferFragment) decide whether
    // to record it. Kept separate from Timber logging since that's for developer debugging,
    // this is for the user-facing raw traffic log.
    var trafficCallback: ((direction: String, data: String) -> Unit)? = null

    // GM extended (Mode 22) PIDs must be requested with the CAN header set to the specific
    // module (ECM/TCM/etc.) that owns them - the header persists across requests on the
    // ELM327 until changed again, so track it to avoid redundant AT commands and to make
    // sure standard Mode 01 PIDs go back to the default functional address afterward.
    private var currentHeader: String = DEFAULT_HEADER

    companion object {
        private const val DEFAULT_HEADER = "7DF" // standard CAN functional/broadcast request ID
    }

    /**
     * Selects which module on the CAN bus subsequent requests target (e.g. "7E0" for the ECM,
     * "7E1"/"7E2" for the TCM depending on platform). Pass "Auto" to restore the default
     * functional addressing used by standard Mode 01 PIDs.
     */
    fun setHeader(header: String) {
        val target = if (header == "Auto") DEFAULT_HEADER else header
        if (target == currentHeader) return
        sendCommand("AT SH $target")
        currentHeader = target
    }

    fun connect(deviceAddress: String) {
        connectionJob = scope.launch {
            try {
                val bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()
                val device = bluetoothAdapter?.getRemoteDevice(deviceAddress)
                    ?: throw IllegalArgumentException("Device not found")

                Timber.d("Connecting to ${device.name} ($deviceAddress)")

                bluetoothSocket = device.createRfcommSocketToServiceRecord(
                    UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
                )

                bluetoothSocket?.connect()
                inputReader = BufferedReader(InputStreamReader(bluetoothSocket?.inputStream))
                outputWriter = OutputStreamWriter(bluetoothSocket?.outputStream)

                isConnected = true
                Timber.i("Bluetooth connected successfully")

                withContext(Dispatchers.Main) {
                    connectionCallback?.invoke(true, null)
                }

                startListening()
            } catch (e: Exception) {
                isConnected = false
                Timber.e(e, "Failed to connect to Bluetooth device")
                withContext(Dispatchers.Main) {
                    connectionCallback?.invoke(false, e.message)
                }
                disconnect()
            }
        }
    }

    private suspend fun startListening() {
        try {
            while (isConnected && inputReader != null) {
                val line = inputReader?.readLine() ?: break
                if (line.isNotEmpty()) {
                    withContext(Dispatchers.Main) {
                        dataCallback?.invoke(line)
                    }
                }
            }
        } catch (e: Exception) {
            Timber.e(e, "Error reading from Bluetooth")
            disconnect()
        }
    }

    /**
     * Send command and read response until ELM327 prompt (">") is received.
     * ELM327 with AT H1 returns: [HEADER] [DATA] [>]
     * This reads all lines until ">" to ensure we get the complete response.
     */
    fun sendCommand(command: String): String? {
        return try {
            if (!isConnected || outputWriter == null || inputReader == null) {
                Timber.w("Bluetooth not connected")
                return null
            }

            synchronized(outputWriter!!) {
                outputWriter?.write(command)
                outputWriter?.write("\r")
                outputWriter?.flush()

                Timber.d("Sent: $command")
                trafficCallback?.invoke("TX", command)

                // Read all lines until prompt (">") - ELM327 may return header + data + prompt
                val startTime = System.currentTimeMillis()
                val timeout = 2000L // 2 second timeout for longer responses
                val responseLines = mutableListOf<String>()
                var foundPrompt = false

                while (System.currentTimeMillis() - startTime < timeout && !foundPrompt) {
                    if (inputReader?.ready() == true) {
                        val line = inputReader?.readLine()
                        if (!line.isNullOrEmpty()) {
                            if (line.trim() == ">") {
                                foundPrompt = true
                                break
                            }
                            responseLines.add(line)
                            Timber.d("Response line: $line")
                        }
                    } else {
                        Thread.sleep(5)
                    }
                }

                // Filter out echo and combine data lines
                val response = responseLines
                    .filter { it.trim() != command && it.isNotEmpty() }
                    .joinToString(" ") // Combine multi-line responses
                    .trim()

                Timber.d("Processed response: $response (${responseLines.size} lines)")
                trafficCallback?.invoke("RX", response)

                response.ifEmpty { null }
            }
        } catch (e: Exception) {
            Timber.e(e, "Error sending OBD2 command")
            null
        }
    }

    fun disconnect() {
        try {
            isConnected = false
            connectionJob?.cancel()
            inputReader?.close()
            outputWriter?.close()
            bluetoothSocket?.close()
            Timber.i("Bluetooth disconnected")
        } catch (e: Exception) {
            Timber.e(e, "Error during disconnect")
        }
    }

    fun initialize(): String? {
        // Initialize ELM327 adapter
        sendCommand("AT Z") // Reset
        Thread.sleep(100)
        sendCommand("AT E0") // Echo off
        Thread.sleep(100)
        sendCommand("AT L0") // Linefeeds off
        Thread.sleep(100)
        sendCommand("AT S0") // Spaces off
        Thread.sleep(100)
        sendCommand("AT H1") // Headers on
        Thread.sleep(100)
        sendCommand("AT CAF0") // CAN automatic formatting off
        Thread.sleep(100)

        // Set protocol 6: ISO 15765-4 CAN, 11-bit ID, 500 kbaud - correct for the E38's CAN bus.
        // (An earlier version of this comment called it KWP2000; that's protocol 4/5, not 6 -
        // E38-era GM vehicles are CAN-based, which is what AT SP6 actually selects.)
        val protocolSet = sendCommand("AT SP6")
        Timber.d("Protocol set: $protocolSet")

        return protocolSet
    }
}
