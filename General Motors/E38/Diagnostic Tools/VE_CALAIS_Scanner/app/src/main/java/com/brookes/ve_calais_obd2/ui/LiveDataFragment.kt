package com.brookes.ve_calais_obd2.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager2.widget.ViewPager2
import com.brookes.ve_calais_obd2.*
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.android.material.switchmaterial.SwitchMaterial
import com.google.android.material.tabs.TabLayoutMediator
import kotlinx.coroutines.*
import timber.log.Timber
import kotlin.random.Random

class LiveDataFragment : Fragment() {

    private val bluetoothManager by lazy { BluetoothSession.get(requireContext()) }
    private val obd2Protocol by lazy { OBD2Protocol(bluetoothManager) }
    private val dataLogger by lazy { DataLogger(requireContext()) }

    private var monitoringJob: Job? = null
    private var isMonitoring = false

    private lateinit var pagerAdapter: DashboardPagerAdapter
    private var currentPages: List<DashboardPage> = emptyList()

    // Simulated values for Demo Mode, so the UI can be tried without a car connected.
    private val demoValues = mutableMapOf<String, Double>()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_live_data, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setupUI(view)
        setupDashboardPager(view)
    }

    override fun onResume() {
        super.onResume()
        // Settings may have changed which sensors/layout are active - rebuild to reflect that.
        view?.let { rebuildDashboard(it) }
    }

    private fun setupUI(view: View) {
        view.findViewById<View>(R.id.btn_toggle_monitoring)?.setOnClickListener {
            if (isMonitoring) stopMonitoring() else startMonitoring()
        }

        view.findViewById<View>(R.id.btn_export_csv)?.setOnClickListener {
            SessionManager.current()?.let { session ->
                dataLogger.exportAsCSV(session)
                showToast("Session exported to CSV")
            } ?: showToast("No active session - connect or start monitoring first")
        }

        view.findViewById<View>(R.id.btn_export_json)?.setOnClickListener {
            SessionManager.current()?.let { session ->
                dataLogger.exportAsJSON(session)
                showToast("Session exported to JSON")
            } ?: showToast("No active session - connect or start monitoring first")
        }
    }

    private fun setupDashboardPager(view: View) {
        val pager = view.findViewById<ViewPager2>(R.id.dashboard_pager)
        val tabs = view.findViewById<com.google.android.material.tabs.TabLayout>(R.id.dashboard_tabs)
        pagerAdapter = DashboardPagerAdapter(emptyList())
        pagerAdapter.onLongPress = { showQuickMenu() }
        pager.adapter = pagerAdapter

        // autoRefresh (default true) keeps tabs in sync whenever pagerAdapter's item count
        // changes later, so this only needs attaching once - not on every rebuildDashboard().
        TabLayoutMediator(tabs, pager) { tab, position ->
            tab.text = currentPages.getOrNull(position)?.title ?: ""
        }.attach()

        rebuildDashboard(view)
    }

    private fun showQuickMenu() {
        val context = requireContext()
        val dialog = BottomSheetDialog(context)
        val sheetView = LayoutInflater.from(context).inflate(R.layout.dialog_quick_menu, null)
        dialog.setContentView(sheetView)

        sheetView.findViewById<SwitchMaterial>(R.id.switch_keep_screen_on)?.apply {
            isChecked = AppPreferences.isKeepScreenOnEnabled(context)
            setOnCheckedChangeListener { _, checked ->
                AppPreferences.setKeepScreenOnEnabled(context, checked)
                applyKeepScreenOn(checked && isMonitoring)
            }
        }
        sheetView.findViewById<SwitchMaterial>(R.id.switch_auto_connect)?.apply {
            isChecked = AppPreferences.isAutoConnectEnabled(context)
            setOnCheckedChangeListener { _, checked ->
                AppPreferences.setAutoConnectEnabled(context, checked)
            }
        }
        sheetView.findViewById<SwitchMaterial>(R.id.switch_sniffer)?.apply {
            isChecked = AppPreferences.isSnifferEnabled(context)
            setOnCheckedChangeListener { _, checked ->
                AppPreferences.setSnifferEnabled(context, checked)
            }
        }
        sheetView.findViewById<SwitchMaterial>(R.id.switch_demo_mode)?.apply {
            isChecked = AppPreferences.isDemoModeEnabled(context)
            setOnCheckedChangeListener { _, checked ->
                AppPreferences.setDemoModeEnabled(context, checked)
                showToast(if (checked) "Demo mode on - showing simulated data" else "Demo mode off")
            }
        }
        sheetView.findViewById<View>(R.id.btn_connect_adapter)?.setOnClickListener {
            dialog.dismiss()
            BluetoothConnectHelper.showDeviceListAndConnect(this) {}
        }
        sheetView.findViewById<View>(R.id.btn_open_scanner)?.setOnClickListener {
            dialog.dismiss()
            findNavController().navigate(R.id.nav_pid_scanner)
        }
        sheetView.findViewById<View>(R.id.btn_open_sniffer)?.setOnClickListener {
            dialog.dismiss()
            findNavController().navigate(R.id.nav_sniffer)
        }
        sheetView.findViewById<View>(R.id.btn_open_dtc)?.setOnClickListener {
            dialog.dismiss()
            findNavController().navigate(R.id.nav_dtc)
        }
        sheetView.findViewById<View>(R.id.btn_reorder_pages)?.setOnClickListener {
            dialog.dismiss()
            showReorderPagesDialog()
        }
        sheetView.findViewById<View>(R.id.btn_open_settings)?.setOnClickListener {
            dialog.dismiss()
            findNavController().navigate(R.id.nav_settings)
        }

        dialog.show()
    }

    private fun showReorderPagesDialog() {
        val context = requireContext()
        val dialog = BottomSheetDialog(context)
        val sheetView = LayoutInflater.from(context).inflate(R.layout.dialog_reorder_pages, null)
        dialog.setContentView(sheetView)

        val monitored = AppPreferences.getMonitoredPIDs(context).mapNotNull { PIDDatabase.getPID(it) }
        val defaultOrder = DashboardPager.defaultPageOrder(monitored)
        val savedOrder = AppPreferences.getPageOrder(context)
        // Start from the saved order, but always include any page titles that exist now and
        // weren't in the saved order yet (e.g. a sensor category added since last reorder).
        val startingOrder = if (savedOrder.isEmpty()) {
            defaultOrder
        } else {
            savedOrder.filter { it in defaultOrder } + defaultOrder.filter { it !in savedOrder }
        }

        val adapter = ReorderPagesAdapter(startingOrder.toMutableList())
        val recycler = sheetView.findViewById<RecyclerView>(R.id.recycler_reorder_pages)
        recycler.layoutManager = LinearLayoutManager(context)
        recycler.adapter = adapter

        sheetView.findViewById<View>(R.id.btn_reorder_reset)?.setOnClickListener {
            adapter.resetTo(defaultOrder)
        }
        sheetView.findViewById<View>(R.id.btn_reorder_save)?.setOnClickListener {
            AppPreferences.setPageOrder(context, adapter.currentOrder())
            dialog.dismiss()
            view?.let { rebuildDashboard(it) }
            showToast("Page order saved")
        }

        dialog.show()
    }

    private fun applyKeepScreenOn(enabled: Boolean) {
        val window = activity?.window ?: return
        if (enabled) {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        } else {
            window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }
    }

    /**
     * Rebuilds the paged dashboard from the monitored-sensor selection (Settings) and applies
     * the chosen layout style (list = 1 column, grid = 2 columns per page).
     */
    private fun rebuildDashboard(view: View) {
        val pager = view.findViewById<ViewPager2>(R.id.dashboard_pager)
        val noReadingsText = view.findViewById<TextView>(R.id.txt_no_readings)

        val monitored = AppPreferences.getMonitoredPIDs(requireContext())
            .mapNotNull { PIDDatabase.getPID(it) }
        val pageOrder = AppPreferences.getPageOrder(requireContext())
        currentPages = DashboardPager.buildPages(monitored, pageOrder)

        noReadingsText?.visibility = if (currentPages.isEmpty()) View.VISIBLE else View.GONE

        val columnCount = when (AppPreferences.getLayoutStyle(requireContext())) {
            LayoutStyle.GRID -> 2
            LayoutStyle.LIST -> 1
        }
        // notifyDataSetChanged() here also drives the TabLayoutMediator's autoRefresh, so tab
        // titles/count stay in sync without re-attaching a new mediator every rebuild.
        pagerAdapter.updatePages(currentPages, columnCount)
        // Keep every page bound (no recycling) - page count here is small (a handful), and it
        // keeps DashboardPagerAdapter's pid->view map from going stale when scrolled off-screen.
        pager.offscreenPageLimit = maxOf(currentPages.size, 1)
    }

    private fun startMonitoring() {
        if (isMonitoring) return

        SessionManager.getOrStartSession(requireContext())

        isMonitoring = true
        updateToggleButton()
        applyKeepScreenOn(AppPreferences.isKeepScreenOnEnabled(requireContext()))
        Timber.i("Starting live data monitoring")

        monitoringJob = lifecycleScope.launch {
            while (isMonitoring) {
                try {
                    monitorPIDs()
                    delay(500) // Update every 500ms
                } catch (e: Exception) {
                    Timber.e(e, "Error during monitoring")
                }
            }
        }
    }

    private suspend fun monitorPIDs() {
        val context = requireContext()
        val demoMode = AppPreferences.isDemoModeEnabled(context)
        val pidsToMonitor = AppPreferences.getMonitoredPIDs(context)
        val readings = mutableMapOf<String, Double>()
        val session = SessionManager.current()

        withContext(Dispatchers.Default) {
            pidsToMonitor.forEach { pidHex ->
                val pidParam = PIDDatabase.getPID(pidHex) ?: return@forEach

                val value = if (demoMode) {
                    nextDemoValue(pidParam)
                } else {
                    val response = obd2Protocol.requestPID(pidParam) ?: return@forEach
                    pidParam.parse(response)
                }

                if (value != null) {
                    readings[pidHex] = value

                    session?.let {
                        val data = mapOf(
                            "PID" to pidHex,
                            "Parameter" to pidParam.name,
                            "Value" to value,
                            "Unit" to pidParam.unit,
                            "Category" to pidParam.category
                        )
                        dataLogger.addEntry(it, data)
                    }
                }
            }
        }

        withContext(Dispatchers.Main) {
            readings.forEach { (pidHex, value) ->
                val pidParam = PIDDatabase.getPID(pidHex) ?: return@forEach
                pagerAdapter.pushValue(pidHex, value, "%.1f %s".format(value, pidParam.unit))
            }
        }
    }

    /** Simple random walk within the PID's declared range, for trying the UI without a car. */
    private fun nextDemoValue(pidParam: PIDParameter): Double {
        val range = (pidParam.max - pidParam.min).let { if (it > 0) it else 1.0 }
        val current = demoValues.getOrPut(pidParam.pid) { pidParam.min + range / 2 }
        val step = range * 0.03 * (Random.nextDouble() - 0.5)
        val next = (current + step).coerceIn(pidParam.min, pidParam.max)
        demoValues[pidParam.pid] = next
        return next
    }

    private fun stopMonitoring() {
        if (!isMonitoring) return

        isMonitoring = false
        updateToggleButton()
        monitoringJob?.cancel()
        applyKeepScreenOn(false)

        // Auto-saves CSV + JSON with date-stamped filenames.
        SessionManager.endCurrentSession(requireContext())

        Timber.i("Stopping live data monitoring")
        showToast("Monitoring stopped - session saved")
    }

    private fun updateToggleButton() {
        val button = view?.findViewById<com.google.android.material.button.MaterialButton>(R.id.btn_toggle_monitoring)
            ?: return
        button.setIconResource(if (isMonitoring) R.drawable.ic_stop else R.drawable.ic_play)
        button.contentDescription = if (isMonitoring) "Stop Monitoring" else "Start Monitoring"
    }

    private fun showToast(message: String) {
        android.widget.Toast.makeText(requireContext(), message, android.widget.Toast.LENGTH_SHORT).show()
    }

    override fun onDestroyView() {
        stopMonitoring()
        super.onDestroyView()
    }
}
