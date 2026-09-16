package com.brookes.ve_calais_obd2.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.brookes.ve_calais_obd2.AppPreferences
import com.brookes.ve_calais_obd2.BluetoothConnectHelper
import com.brookes.ve_calais_obd2.BluetoothSession
import com.brookes.ve_calais_obd2.R
import com.google.android.material.switchmaterial.SwitchMaterial

/**
 * Home tab: connection status, adapter connect, and the operational toggles - everything that
 * isn't a sensor reading lives here now, so the Live Data screen can be PIDs-only.
 */
class HomeFragment : Fragment() {

    private val bluetoothManager by lazy { BluetoothSession.get(requireContext()) }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_home, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        updateConnectionStatusUI(bluetoothManager.isConnected)

        view.findViewById<View>(R.id.btn_home_connect)?.setOnClickListener {
            BluetoothConnectHelper.showDeviceListAndConnect(this) { connected -> updateConnectionStatusUI(connected) }
        }
        view.findViewById<View>(R.id.btn_home_live_data)?.setOnClickListener {
            findNavController().navigate(R.id.nav_live_data)
        }
        view.findViewById<View>(R.id.btn_home_scanner)?.setOnClickListener {
            findNavController().navigate(R.id.nav_pid_scanner)
        }
        view.findViewById<View>(R.id.btn_home_sniffer)?.setOnClickListener {
            findNavController().navigate(R.id.nav_sniffer)
        }
        view.findViewById<View>(R.id.btn_home_dtc)?.setOnClickListener {
            findNavController().navigate(R.id.nav_dtc)
        }

        val context = requireContext()
        view.findViewById<SwitchMaterial>(R.id.home_switch_keep_screen_on)?.apply {
            isChecked = AppPreferences.isKeepScreenOnEnabled(context)
            setOnCheckedChangeListener { _, checked -> AppPreferences.setKeepScreenOnEnabled(context, checked) }
        }
        view.findViewById<SwitchMaterial>(R.id.home_switch_auto_connect)?.apply {
            isChecked = AppPreferences.isAutoConnectEnabled(context)
            setOnCheckedChangeListener { _, checked -> AppPreferences.setAutoConnectEnabled(context, checked) }
        }
        view.findViewById<SwitchMaterial>(R.id.home_switch_demo_mode)?.apply {
            isChecked = AppPreferences.isDemoModeEnabled(context)
            setOnCheckedChangeListener { _, checked -> AppPreferences.setDemoModeEnabled(context, checked) }
        }
    }

    override fun onResume() {
        super.onResume()
        updateConnectionStatusUI(bluetoothManager.isConnected)
    }

    private fun updateConnectionStatusUI(connected: Boolean) {
        val view = view ?: return
        view.findViewById<View>(R.id.home_status_indicator)?.setBackgroundResource(
            if (connected) R.drawable.circle_green else R.drawable.circle_red
        )
        view.findViewById<TextView>(R.id.txt_home_connection_status)?.text =
            if (connected) "Connected" else "Not Connected"
    }
}
