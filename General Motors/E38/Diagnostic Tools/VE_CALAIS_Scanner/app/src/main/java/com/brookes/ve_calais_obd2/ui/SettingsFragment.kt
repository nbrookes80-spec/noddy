package com.brookes.ve_calais_obd2.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.CheckBox
import android.widget.LinearLayout
import android.widget.RadioGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import com.brookes.ve_calais_obd2.AppPreferences
import com.brookes.ve_calais_obd2.LayoutStyle
import com.brookes.ve_calais_obd2.PIDDatabase
import com.brookes.ve_calais_obd2.R

/** Settings tab: display layout and which sensors are monitored. Connection/adapter/tools
 * live on the Home tab instead - see HomeFragment. */
class SettingsFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_settings, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupLayoutStyleToggle(view)
        buildSensorChecklist(view)
    }

    private fun setupLayoutStyleToggle(view: View) {
        val radioGroup = view.findViewById<RadioGroup>(R.id.radio_layout_style)
        val listRadio = view.findViewById<View>(R.id.radio_layout_list)
        val gridRadio = view.findViewById<View>(R.id.radio_layout_grid)

        when (AppPreferences.getLayoutStyle(requireContext())) {
            LayoutStyle.LIST -> radioGroup.check(listRadio.id)
            LayoutStyle.GRID -> radioGroup.check(gridRadio.id)
        }

        radioGroup.setOnCheckedChangeListener { _, checkedId ->
            val style = if (checkedId == gridRadio.id) LayoutStyle.GRID else LayoutStyle.LIST
            AppPreferences.setLayoutStyle(requireContext(), style)
        }
    }

    private fun buildSensorChecklist(view: View) {
        val container = view.findViewById<LinearLayout>(R.id.sensor_checklist_container)
        container.removeAllViews()

        val monitored = AppPreferences.getMonitoredPIDs(requireContext()).toMutableSet()
        val byCategory = PIDDatabase.getAllPIDs()
            .sortedBy { it.name }
            .groupBy { it.category }
            .toSortedMap()

        byCategory.forEach { (category, pids) ->
            val header = TextView(requireContext()).apply {
                text = category
                textSize = 14f
                setTextColor(resources.getColor(android.R.color.darker_gray, null))
                setPadding(0, 24, 0, 4)
            }
            container.addView(header)

            pids.forEach { pidParam ->
                val checkBox = CheckBox(requireContext()).apply {
                    text = "${pidParam.name} (${pidParam.unit})"
                    isChecked = monitored.contains(pidParam.pid)
                    setOnCheckedChangeListener { _, isChecked ->
                        val current = AppPreferences.getMonitoredPIDs(requireContext()).toMutableSet()
                        if (isChecked) current.add(pidParam.pid) else current.remove(pidParam.pid)
                        AppPreferences.setMonitoredPIDs(requireContext(), current)
                    }
                }
                container.addView(checkBox)
            }
        }
    }
}
