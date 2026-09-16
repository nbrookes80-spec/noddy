package com.brookes.ve_calais_obd2.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.brookes.ve_calais_obd2.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * In-app port of did_sweeper.py: sweeps Mode 22 DIDs on a chosen module header, using the
 * app's own Bluetooth connection instead of a laptop + TorqueScan Telnet bridge.
 */
class PidScannerFragment : Fragment() {

    private val bluetoothManager by lazy { BluetoothSession.get(requireContext()) }
    private val dataLogger by lazy { DataLogger(requireContext()) }

    private var scanJob: Job? = null
    private var lastResults: List<ScanRecord> = emptyList()
    private val logBuilder = StringBuilder()

    private val planOptions = listOf(
        "All 3 modules (full protocol)" to PidScanner.DEFAULT_PLAN,
        "7E2 - T43 TCM only" to PidScanner.DEFAULT_PLAN.filter { it.header == "7E2" },
        "7E0 - E38 ECM only" to PidScanner.DEFAULT_PLAN.filter { it.header == "7E0" },
        "7E3 - FPCM only" to PidScanner.DEFAULT_PLAN.filter { it.header == "7E3" }
    )

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_pid_scanner, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val spinner = view.findViewById<Spinner>(R.id.spinner_scan_plan)
        spinner.adapter = ArrayAdapter(
            requireContext(),
            android.R.layout.simple_spinner_item,
            planOptions.map { it.first }
        ).also { it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item) }

        view.findViewById<View>(R.id.btn_start_scan).setOnClickListener {
            val plan = planOptions[spinner.selectedItemPosition].second
            startScan(plan)
        }
        view.findViewById<View>(R.id.btn_stop_scan).setOnClickListener { stopScan() }
        view.findViewById<View>(R.id.btn_export_scan).setOnClickListener { exportResults() }
    }

    private fun startScan(plan: List<ScanBlock>) {
        if (scanJob?.isActive == true) return
        if (!bluetoothManager.isConnected) {
            showToast("Not connected - connect to the OBD2 adapter from the dashboard's long-press menu first")
            return
        }

        logBuilder.clear()
        appendLog("Starting scan: ${plan.joinToString { it.header }}")
        lastResults = emptyList()

        scanJob = lifecycleScope.launch(Dispatchers.IO) {
            val total = PidScanner.totalRequests(plan)
            val results = mutableListOf<ScanRecord>()
            var done = 0
            var hits = 0
            val startTime = System.currentTimeMillis()

            for (block in plan) {
                if (!isActive) break
                bluetoothManager.setHeader(block.header)
                appendLog("=== ${block.header} (${block.label}) ===")

                for (hi in block.highBytes) {
                    if (!isActive) break
                    var foundInBlock = 0

                    for (lo in 0..255) {
                        if (!isActive) break
                        val did = "%02X%02X".format(hi, lo)
                        val raw = bluetoothManager.sendCommand("22$did") ?: ""
                        val (status, detail) = PidScanner.classify(did, raw)

                        if (status == "SUPPORTED") {
                            hits++
                            foundInBlock++
                            results.add(ScanRecord(block.header, did, status, detail, block.label))
                            appendLog("*** $did @ ${block.header}  data=$detail")
                        } else if (status != "REJECTED_31") {
                            // Drop pure "doesn't exist" noise, same as did_sweeper.py's CSV filter
                            results.add(ScanRecord(block.header, did, status, detail, block.label))
                        }

                        done++
                        if (done % 32 == 0) {
                            val elapsed = (System.currentTimeMillis() - startTime) / 1000.0
                            val rate = if (elapsed > 0) done / elapsed else 0.0
                            val eta = if (rate > 0) (total - done) / rate else 0.0
                            updateProgress(done, total, rate, eta)
                        }
                    }

                    appendLog("block 0x%02Xxx: %d supported".format(hi, foundInBlock))
                }
            }

            lastResults = results
            withContext(Dispatchers.Main) {
                val status = view?.findViewById<TextView>(R.id.txt_scan_status)
                status?.text = "Complete - $hits supported DID(s) found across $done requests"
                showToast("Scan complete: $hits supported DIDs found")
            }
        }
    }

    private fun stopScan() {
        scanJob?.cancel()
        appendLog("--- Stopped by user ---")
    }

    private fun exportResults() {
        if (lastResults.isEmpty()) {
            showToast("No scan results yet")
            return
        }
        val success = dataLogger.exportScanResults(lastResults)
        showToast(if (success) "Exported to ${dataLogger.getLogsDirectoryPath()}" else "Export failed")
    }

    private suspend fun updateProgress(done: Int, total: Int, rate: Double, eta: Double) {
        withContext(Dispatchers.Main) {
            val view = view ?: return@withContext
            view.findViewById<ProgressBar>(R.id.scan_progress)?.progress =
                if (total > 0) (done * 100 / total) else 0
            view.findViewById<TextView>(R.id.txt_scan_status)?.text =
                "Scanning... %d/%d  (%.1f/s, ETA %.0fs)".format(done, total, rate, eta)
        }
    }

    private fun appendLog(line: String) {
        logBuilder.append(line).append("\n")
        lifecycleScope.launch(Dispatchers.Main) {
            val logView = view?.findViewById<TextView>(R.id.txt_scan_log) ?: return@launch
            logView.text = logBuilder.toString()
            (logView.parent as? ScrollView)?.post {
                (logView.parent as? ScrollView)?.fullScroll(View.FOCUS_DOWN)
            }
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(requireContext(), message, Toast.LENGTH_SHORT).show()
    }

    override fun onDestroyView() {
        scanJob?.cancel()
        super.onDestroyView()
    }
}
