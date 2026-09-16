package com.brookes.ve_calais_obd2.ui

import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.GridLayout
import android.widget.ScrollView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.brookes.ve_calais_obd2.DashboardPage
import com.brookes.ve_calais_obd2.R
import com.github.mikephil.charting.charts.BarChart
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.data.BarData
import com.github.mikephil.charting.data.BarDataSet
import com.github.mikephil.charting.data.BarEntry
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet

private const val MAX_HISTORY = 40
private val ACCENT_COLOR = Color.parseColor("#4CAF50")

enum class DisplayMode { DIGITAL, GRAPH, HISTOGRAM }

/**
 * Renders one dashboard page (up to 4 sensor cards) per ViewPager2 position. Each page is
 * wrapped in its own vertical ScrollView so a page's cards can never be clipped by the fixed
 * pager height (previously they were, with no way to reach cards past the fold). Tapping a
 * card cycles it through Digital -> Graph -> Histogram, matching how Torque Pro lets you
 * change a gauge's display type and AndrOBD's separate dashboard/chart views.
 */
class DashboardPagerAdapter(
    private var pages: List<DashboardPage>,
    private var columnCount: Int = 2
) : RecyclerView.Adapter<DashboardPagerAdapter.PageViewHolder>() {

    private class CardRefs(
        val nameText: TextView,
        val valueText: TextView,
        val lineChart: LineChart,
        val barChart: BarChart,
        var mode: DisplayMode = DisplayMode.DIGITAL
    )

    // pid -> its currently-bound card. Callers must set the ViewPager2's offscreenPageLimit to
    // pages.size so every page stays bound (no recycling), otherwise these go stale when a
    // far-off page is recycled and rebound elsewhere.
    private val cards = mutableMapOf<String, CardRefs>()
    private val history = mutableMapOf<String, MutableList<Float>>()

    var onLongPress: (() -> Unit)? = null

    class PageViewHolder(val scroll: ScrollView, val grid: GridLayout) : RecyclerView.ViewHolder(scroll)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PageViewHolder {
        val grid = GridLayout(parent.context).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT
            )
            setPadding(24, 24, 24, 24)
        }
        grid.setOnLongClickListener {
            onLongPress?.invoke()
            true
        }
        val scroll = ScrollView(parent.context).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
            isFillViewport = true
            addView(grid)
        }
        return PageViewHolder(scroll, grid)
    }

    override fun onBindViewHolder(holder: PageViewHolder, position: Int) {
        val page = pages[position]
        holder.grid.removeAllViews()
        holder.grid.columnCount = columnCount
        val inflater = LayoutInflater.from(holder.grid.context)

        page.pids.forEach { pidParam ->
            val row: View = inflater.inflate(R.layout.item_pid_reading, holder.grid, false)
            val nameText = row.findViewById<TextView>(R.id.item_pid_name)
            val valueText = row.findViewById<TextView>(R.id.item_pid_value)
            val lineChart = row.findViewById<LineChart>(R.id.item_pid_chart_line)
            val barChart = row.findViewById<BarChart>(R.id.item_pid_chart_bar)

            nameText.text = pidParam.name
            valueText.text = "--"
            configureChart(lineChart)
            configureChart(barChart)

            val refs = CardRefs(nameText, valueText, lineChart, barChart)
            cards[pidParam.pid] = refs
            applyMode(pidParam.pid, refs)

            row.setOnClickListener {
                refs.mode = when (refs.mode) {
                    DisplayMode.DIGITAL -> DisplayMode.GRAPH
                    DisplayMode.GRAPH -> DisplayMode.HISTOGRAM
                    DisplayMode.HISTOGRAM -> DisplayMode.DIGITAL
                }
                applyMode(pidParam.pid, refs)
            }
            row.setOnLongClickListener {
                onLongPress?.invoke()
                true
            }

            val lp = GridLayout.LayoutParams().apply {
                width = 0
                height = GridLayout.LayoutParams.WRAP_CONTENT
                columnSpec = GridLayout.spec(GridLayout.UNDEFINED, 1f)
                rowSpec = GridLayout.spec(GridLayout.UNDEFINED)
                setMargins(8, 8, 8, 8)
            }
            row.layoutParams = lp
            holder.grid.addView(row)
        }
    }

    override fun getItemCount(): Int = pages.size

    fun updatePages(newPages: List<DashboardPage>, newColumnCount: Int = columnCount) {
        pages = newPages
        columnCount = newColumnCount
        cards.clear()
        notifyDataSetChanged()
    }

    /** Called on every reading: updates the digital text and appends to that PID's chart history. */
    fun pushValue(pid: String, value: Double, formattedText: String) {
        val buffer = history.getOrPut(pid) { mutableListOf() }
        buffer.add(value.toFloat())
        if (buffer.size > MAX_HISTORY) buffer.removeAt(0)

        val refs = cards[pid] ?: return
        when (refs.mode) {
            DisplayMode.DIGITAL -> refs.valueText.text = formattedText
            DisplayMode.GRAPH -> updateLineChart(refs.lineChart, buffer)
            DisplayMode.HISTOGRAM -> updateBarChart(refs.barChart, buffer)
        }
    }

    private fun applyMode(pid: String, refs: CardRefs) {
        refs.valueText.visibility = if (refs.mode == DisplayMode.DIGITAL) View.VISIBLE else View.GONE
        refs.lineChart.visibility = if (refs.mode == DisplayMode.GRAPH) View.VISIBLE else View.GONE
        refs.barChart.visibility = if (refs.mode == DisplayMode.HISTOGRAM) View.VISIBLE else View.GONE

        val buffer = history[pid] ?: return
        when (refs.mode) {
            DisplayMode.GRAPH -> updateLineChart(refs.lineChart, buffer)
            DisplayMode.HISTOGRAM -> updateBarChart(refs.barChart, buffer)
            DisplayMode.DIGITAL -> {}
        }
    }

    private fun configureChart(chart: com.github.mikephil.charting.charts.Chart<*>) {
        chart.description.isEnabled = false
        chart.legend.isEnabled = false
        chart.setTouchEnabled(false)
        chart.setNoDataText("")
        if (chart is LineChart) {
            chart.axisRight.isEnabled = false
            chart.axisLeft.textColor = Color.WHITE
            chart.axisLeft.textSize = 8f
            chart.xAxis.isEnabled = false
        }
        if (chart is BarChart) {
            chart.axisRight.isEnabled = false
            chart.axisLeft.textColor = Color.WHITE
            chart.axisLeft.textSize = 8f
            chart.xAxis.isEnabled = false
        }
    }

    private fun updateLineChart(chart: LineChart, values: List<Float>) {
        val entries = values.mapIndexed { i, v -> Entry(i.toFloat(), v) }
        val dataSet = LineDataSet(entries, "").apply {
            setDrawCircles(false)
            setDrawValues(false)
            color = ACCENT_COLOR
            lineWidth = 2f
        }
        chart.data = LineData(dataSet)
        chart.invalidate()
    }

    private fun updateBarChart(chart: BarChart, values: List<Float>) {
        val entries = values.mapIndexed { i, v -> BarEntry(i.toFloat(), v) }
        val dataSet = BarDataSet(entries, "").apply {
            color = ACCENT_COLOR
            setDrawValues(false)
        }
        chart.data = BarData(dataSet)
        chart.invalidate()
    }
}
