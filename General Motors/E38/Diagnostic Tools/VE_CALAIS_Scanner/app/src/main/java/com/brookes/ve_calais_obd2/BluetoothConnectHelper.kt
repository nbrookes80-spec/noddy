package com.brookes.ve_calais_obd2

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.content.pm.PackageManager
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

/**
 * Paired-device picker + connect flow, shared by the Live Data quick menu and the Settings
 * screen so there are two independent, discoverable paths to it (not just a long-press gesture).
 */
object BluetoothConnectHelper {

    @Suppress("MissingPermission")
    fun showDeviceListAndConnect(fragment: Fragment, onStatusChanged: (Boolean) -> Unit) {
        val context = fragment.requireContext()
        if (ActivityCompat.checkSelfPermission(context, Manifest.permission.BLUETOOTH_CONNECT)
            != PackageManager.PERMISSION_GRANTED
        ) {
            Toast.makeText(context, "Bluetooth permission not granted", Toast.LENGTH_SHORT).show()
            return
        }

        val paired = BluetoothAdapter.getDefaultAdapter()?.bondedDevices?.toList() ?: emptyList()
        if (paired.isEmpty()) {
            Toast.makeText(
                context,
                "No paired devices - pair your OBD2 adapter in phone Settings > Bluetooth first",
                Toast.LENGTH_LONG
            ).show()
            return
        }

        val names = paired.map { it.name ?: it.address }.toTypedArray()
        MaterialAlertDialogBuilder(context)
            .setTitle("Select OBD2 Adapter")
            .setItems(names) { _, which -> connect(fragment, paired[which].address, onStatusChanged) }
            .show()
    }

    private fun connect(fragment: Fragment, address: String, onStatusChanged: (Boolean) -> Unit) {
        val context = fragment.requireContext()
        val manager = BluetoothSession.get(context)
        manager.connectionCallback = { connected, error ->
            if (connected) {
                // initialize() sends several blocking AT commands - keep it off the main thread
                fragment.lifecycleScope.launch(Dispatchers.IO) { manager.initialize() }
                // A fresh log session starts on every successful connection, auto-saved
                // (CSV + JSON, date-stamped) when it ends - no manual export required.
                SessionManager.startNewSession(context)
                Toast.makeText(context, "Connected - logging session started", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(context, "Connection failed: ${error ?: "unknown error"}", Toast.LENGTH_SHORT).show()
            }
            onStatusChanged(connected)
        }
        Toast.makeText(context, "Connecting...", Toast.LENGTH_SHORT).show()
        manager.connect(address)
    }
}
