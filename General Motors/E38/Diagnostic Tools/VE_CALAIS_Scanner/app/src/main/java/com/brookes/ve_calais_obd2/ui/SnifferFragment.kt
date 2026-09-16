package com.brookes.ve_calais_obd2.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ScrollView
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.brookes.ve_calais_obd2.AppPreferences
import com.brookes.ve_calais_obd2.BluetoothSession
import com.brookes.ve_calais_obd2.R
import com.google.android.material.switchmaterial.SwitchMaterial
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/** Live raw TX/RX traffic log, for debugging adapter/header issues (e.g. confirming ATSH works). */
class SnifferFragment : Fragment() {

    private val bluetoothManager by lazy { BluetoothSession.get(requireContext()) }
    private val logBuilder = StringBuilder()
    private val timeFormat = SimpleDateFormat("HH:mm:ss.SSS", Locale.US)

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_sniffer, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val switch = view.findViewById<SwitchMaterial>(R.id.switch_sniffer_enabled)
        switch.isChecked = AppPreferences.isSnifferEnabled(requireContext())
        applyCaptureState(switch.isChecked)

        switch.setOnCheckedChangeListener { _, checked ->
            AppPreferences.setSnifferEnabled(requireContext(), checked)
            applyCaptureState(checked)
        }

        view.findViewById<View>(R.id.btn_clear_sniffer).setOnClickListener {
            logBuilder.clear()
            view.findViewById<TextView>(R.id.txt_sniffer_log)?.text = "Waiting for traffic..."
        }
    }

    private fun applyCaptureState(enabled: Boolean) {
        bluetoothManager.trafficCallback = if (enabled) {
            { direction, data -> onTraffic(direction, data) }
        } else {
            null
        }
    }

    private fun onTraffic(direction: String, data: String) {
        val line = "${timeFormat.format(Date())}  $direction  $data"
        logBuilder.append(line).append("\n")
        lifecycleScope.launch(Dispatchers.Main) {
            val logView = view?.findViewById<TextView>(R.id.txt_sniffer_log) ?: return@launch
            logView.text = logBuilder.toString()
            (logView.parent as? ScrollView)?.post {
                (logView.parent as? ScrollView)?.fullScroll(View.FOCUS_DOWN)
            }
        }
    }

    override fun onDestroyView() {
        bluetoothManager.trafficCallback = null
        super.onDestroyView()
    }
}
