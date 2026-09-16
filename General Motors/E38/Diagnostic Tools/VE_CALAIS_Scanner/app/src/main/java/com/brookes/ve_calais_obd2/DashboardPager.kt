package com.brookes.ve_calais_obd2

data class DashboardPage(val title: String, val pids: List<PIDParameter>)

/**
 * Groups the monitored sensors into swipeable pages of at most 4, titled by system
 * (Engine, Fuel, TCM, etc.) rather than the raw PID category string. A cross-cutting
 * "Thermal" page comes first, pulling every temperature sensor regardless of category -
 * useful since heat (coolant/oil/trans/intake) is the thing you actually watch together.
 */
object DashboardPager {

    private const val PAGE_SIZE = 4

    /**
     * @param pageOrder user's saved order of base page titles (e.g. ["TCM", "Thermal", "Engine"]),
     * from [AppPreferences.getPageOrder]. Empty = use the default order below. Any page whose
     * base title isn't in [pageOrder] (e.g. a page that only appeared because more sensors were
     * added since the order was saved) is appended after the ordered ones, in default order.
     */
    fun buildPages(monitoredPids: List<PIDParameter>, pageOrder: List<String> = emptyList()): List<DashboardPage> {
        val pages = mutableListOf<DashboardPage>()

        val thermal = monitoredPids.filter { it.unit == "°C" }
        pages += chunk(thermal, "Thermal")

        val remaining = monitoredPids - thermal.toSet()
        val byPageTitle = remaining.groupBy { pageTitleFor(it.category) }
        byPageTitle.toSortedMap().forEach { (title, pids) ->
            pages += chunk(pids, title)
        }

        if (pageOrder.isEmpty()) return pages
        return applyPageOrder(pages, pageOrder)
    }

    /** Base title without the " (n/m)" multi-chunk suffix, used to key the saved order. */
    fun baseTitle(pageTitle: String): String = pageTitle.substringBefore(" (")

    /** Every distinct base title currently on the dashboard, in their default (unordered) sequence. */
    fun defaultPageOrder(monitoredPids: List<PIDParameter>): List<String> {
        return buildPages(monitoredPids).map { baseTitle(it.title) }.distinct()
    }

    private fun applyPageOrder(pages: List<DashboardPage>, pageOrder: List<String>): List<DashboardPage> {
        val grouped = pages.groupBy { baseTitle(it.title) }
        val ordered = mutableListOf<DashboardPage>()
        pageOrder.forEach { title -> grouped[title]?.let { ordered += it } }
        val orderedTitles = pageOrder.toSet()
        grouped.forEach { (title, group) -> if (title !in orderedTitles) ordered += group }
        return ordered
    }

    private fun pageTitleFor(category: String): String = when {
        category.startsWith("Transmission") -> "TCM"
        else -> category
    }

    private fun chunk(pids: List<PIDParameter>, title: String): List<DashboardPage> {
        if (pids.isEmpty()) return emptyList()
        val sorted = pids.sortedBy { it.name }
        val groups = sorted.chunked(PAGE_SIZE)
        return groups.mapIndexed { i, group ->
            val suffix = if (groups.size > 1) " (${i + 1}/${groups.size})" else ""
            DashboardPage(title + suffix, group)
        }
    }
}
