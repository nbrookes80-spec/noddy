package com.brookes.ve_calais_obd2

import android.content.Context

enum class LayoutStyle { LIST, GRID }

/**
 * Shared preferences for which sensors are monitored and how the live data screen is laid out.
 * Read by LiveDataFragment, written by SettingsFragment.
 */
object AppPreferences {

    private const val PREFS_NAME = "ve_calais_settings"
    private const val KEY_MONITORED_PIDS = "monitored_pids"
    private const val KEY_LAYOUT_STYLE = "layout_style"
    private const val KEY_AUTO_CONNECT = "auto_connect"
    private const val KEY_KEEP_SCREEN_ON = "keep_screen_on"
    private const val KEY_SNIFFER_ENABLED = "sniffer_enabled"
    private const val KEY_DEMO_MODE = "demo_mode"
    private const val KEY_PAGE_ORDER = "dashboard_page_order"

    private fun prefs(context: Context) =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun getMonitoredPIDs(context: Context): Set<String> {
        return prefs(context).getStringSet(KEY_MONITORED_PIDS, null)
            ?: PIDDatabase.getMonitoringPIDs().toSet()
    }

    fun setMonitoredPIDs(context: Context, pids: Set<String>) {
        prefs(context).edit().putStringSet(KEY_MONITORED_PIDS, pids).apply()
    }

    fun getLayoutStyle(context: Context): LayoutStyle {
        val stored = prefs(context).getString(KEY_LAYOUT_STYLE, LayoutStyle.LIST.name)
        return try {
            LayoutStyle.valueOf(stored ?: LayoutStyle.LIST.name)
        } catch (e: IllegalArgumentException) {
            LayoutStyle.LIST
        }
    }

    fun setLayoutStyle(context: Context, style: LayoutStyle) {
        prefs(context).edit().putString(KEY_LAYOUT_STYLE, style.name).apply()
    }

    // --- Quick-menu toggles (long-press on the Live Data dashboard) ---

    fun isAutoConnectEnabled(context: Context): Boolean =
        prefs(context).getBoolean(KEY_AUTO_CONNECT, false)

    fun setAutoConnectEnabled(context: Context, enabled: Boolean) {
        prefs(context).edit().putBoolean(KEY_AUTO_CONNECT, enabled).apply()
    }

    fun isKeepScreenOnEnabled(context: Context): Boolean =
        prefs(context).getBoolean(KEY_KEEP_SCREEN_ON, true)

    fun setKeepScreenOnEnabled(context: Context, enabled: Boolean) {
        prefs(context).edit().putBoolean(KEY_KEEP_SCREEN_ON, enabled).apply()
    }

    /** Raw TX/RX traffic logging - off by default since it's a debugging aid, not everyday use. */
    fun isSnifferEnabled(context: Context): Boolean =
        prefs(context).getBoolean(KEY_SNIFFER_ENABLED, false)

    fun setSnifferEnabled(context: Context, enabled: Boolean) {
        prefs(context).edit().putBoolean(KEY_SNIFFER_ENABLED, enabled).apply()
    }

    /** Simulated/demo data instead of a real adapter - useful for trying the car without the car. */
    fun isDemoModeEnabled(context: Context): Boolean =
        prefs(context).getBoolean(KEY_DEMO_MODE, false)

    fun setDemoModeEnabled(context: Context, enabled: Boolean) {
        prefs(context).edit().putBoolean(KEY_DEMO_MODE, enabled).apply()
    }

    /**
     * User's chosen order for dashboard pages (by base category title, e.g. "Thermal", "Engine",
     * "TCM" - without the " (1/2)" multi-chunk suffix). Empty means "no custom order set yet" -
     * DashboardPager falls back to its default alphabetical/Thermal-first order. Stored as a
     * delimited string since SharedPreferences string sets don't preserve order.
     */
    fun getPageOrder(context: Context): List<String> {
        val stored = prefs(context).getString(KEY_PAGE_ORDER, null) ?: return emptyList()
        return stored.split("").filter { it.isNotBlank() }
    }

    fun setPageOrder(context: Context, order: List<String>) {
        prefs(context).edit().putString(KEY_PAGE_ORDER, order.joinToString("")).apply()
    }
}
