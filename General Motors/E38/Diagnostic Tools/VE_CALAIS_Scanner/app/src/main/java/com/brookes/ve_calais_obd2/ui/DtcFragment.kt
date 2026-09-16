package com.brookes.ve_calais_obd2.ui

import android.app.AlertDialog
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.brookes.ve_calais_obd2.BluetoothSession
import com.brookes.ve_calais_obd2.DataLogger
import com.brookes.ve_calais_obd2.OBD2Protocol
import com.brookes.ve_calais_obd2.R
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * Diagnostic Trouble Code read/clear via standard SAE Mode 03/04 - the one write-capable
 * feature in this session's scope that's actually standard and safe to expose today. GM
 * bi-directional actuator tests and module coding are a separate, higher-risk phase (they need
 * per-module routine IDs confirmed via the PID Scanner's DID sweep before they can be trusted,
 * and aren't wired up yet).
 */
class DtcFragment : Fragment() {

    private val bluetoothManager by lazy { BluetoothSession.get(requireContext()) }
    private val obd2Protocol by lazy { OBD2Protocol(bluetoothManager) }
    private val dataLogger by lazy { DataLogger(requireContext()) }

    private var lastReadCodes: List<String> = emptyList()
    private var hasReadOnce = false

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_dtc, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<View>(R.id.btn_read_dtc).setOnClickListener { readCodes() }
        view.findViewById<View>(R.id.btn_clear_dtc).setOnClickListener { confirmClearCodes() }
        view.findViewById<View>(R.id.btn_export_dtc).setOnClickListener { exportResults() }
    }

    private fun readCodes() {
        if (!bluetoothManager.isConnected) {
            showToast("Not connected - connect to the OBD2 adapter from the dashboard's long-press menu first")
            return
        }

        setStatus("Reading codes...")
        lifecycleScope.launch(Dispatchers.IO) {
            val codes = obd2Protocol.readStandardDTCs()
            withContext(Dispatchers.Main) {
                if (codes == null) {
                    setStatus("Read failed - no response from ECU")
                    showResults("Read failed. Check the connection and try again.")
                    return@withContext
                }
                lastReadCodes = codes
                hasReadOnce = true
                if (codes.isEmpty()) {
                    setStatus("Read complete - no stored codes")
                    showResults("No stored DTCs. Vehicle currently reports no faults on this module.")
                } else {
                    setStatus("Read complete - ${codes.size} code(s) found")
                    showResults(codes.joinToString("\n") { "  $it" })
                }
            }
        }
    }

    private fun confirmClearCodes() {
        if (!bluetoothManager.isConnected) {
            showToast("Not connected - connect to the OBD2 adapter from the dashboard's long-press menu first")
            return
        }

        AlertDialog.Builder(requireContext())
            .setTitle("Clear Diagnostic Codes?")
            .setMessage(
                "This sends Mode 04 to the ECU: it erases all stored DTCs, turns off the check " +
                    "engine light, and resets the readiness monitors (they'll need a drive cycle " +
                    "to re-set). This cannot be undone.\n\n" +
                    if (!hasReadOnce) "You haven't read codes yet this session - consider reading first so you have a record of what was cleared." else ""
            )
            .setPositiveButton("Clear Codes") { _, _ -> clearCodes() }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun clearCodes() {
        setStatus("Clearing codes...")
        lifecycleScope.launch(Dispatchers.IO) {
            val success = obd2Protocol.clearStandardDTCs()
            withContext(Dispatchers.Main) {
                if (success) {
                    setStatus("Codes cleared - MIL reset, monitors need a drive cycle")
                    showResults("Codes cleared successfully.")
                    lastReadCodes = emptyList()
                    showToast("DTCs cleared")
                } else {
                    setStatus("Clear failed - no confirmation from ECU")
                    showToast("Clear failed - check the connection and try again")
                }
            }
        }
    }

    private fun exportResults() {
        if (!hasReadOnce) {
            showToast("Read codes first - nothing to export yet")
            return
        }
        val success = dataLogger.exportDtcResults(lastReadCodes)
        showToast(if (success) "Exported to ${dataLogger.getLogsDirectoryPath()}" else "Export failed")
    }

    private fun setStatus(text: String) {
        view?.findViewById<TextView>(R.id.txt_dtc_status)?.text = text
    }

    private fun showResults(text: String) {
        view?.findViewById<TextView>(R.id.txt_dtc_results)?.text = text
    }

    private fun showToast(message: String) {
        Toast.makeText(requireContext(), message, Toast.LENGTH_SHORT).show()
    }
}
