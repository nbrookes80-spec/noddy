package com.brookes.ve_calais_obd2.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.ImageButton
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.brookes.ve_calais_obd2.R
import java.util.Collections

/**
 * Backs the "Reorder Pages" dialog: a list of dashboard page titles with Up/Down buttons per
 * row. This is the first slice of the Torque Pro-style layout customization - full per-cell
 * drag/drop/resize is a bigger follow-up.
 *
 * Uses explicit Up/Down buttons rather than drag-and-drop: a real finger drag would likely work
 * fine, but it couldn't be reliably verified against the running app, and buttons are also more
 * usable one-handed in a car than a precise drag gesture.
 */
class ReorderPagesAdapter(
    private val titles: MutableList<String>
) : RecyclerView.Adapter<ReorderPagesAdapter.ViewHolder>() {

    class ViewHolder(itemView: android.view.View) : RecyclerView.ViewHolder(itemView) {
        val title: TextView = itemView.findViewById(R.id.txt_reorder_page_title)
        val up: ImageButton = itemView.findViewById(R.id.btn_move_up)
        val down: ImageButton = itemView.findViewById(R.id.btn_move_down)
    }

    fun currentOrder(): List<String> = titles.toList()

    fun resetTo(newTitles: List<String>) {
        titles.clear()
        titles.addAll(newTitles)
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_reorder_page, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.title.text = titles[position]
        holder.up.isEnabled = position > 0
        holder.up.alpha = if (position > 0) 1.0f else 0.3f
        holder.down.isEnabled = position < titles.size - 1
        holder.down.alpha = if (position < titles.size - 1) 1.0f else 0.3f

        holder.up.setOnClickListener {
            val pos = holder.bindingAdapterPosition
            if (pos > 0) moveItem(pos, pos - 1)
        }
        holder.down.setOnClickListener {
            val pos = holder.bindingAdapterPosition
            if (pos < titles.size - 1) moveItem(pos, pos + 1)
        }
    }

    override fun getItemCount(): Int = titles.size

    private fun moveItem(fromPosition: Int, toPosition: Int) {
        Collections.swap(titles, fromPosition, toPosition)
        // Both rows' enabled/disabled arrow state can change (e.g. moving to/from the top or
        // bottom), so refresh the two affected rows rather than just notifyItemMoved.
        notifyItemChanged(fromPosition)
        notifyItemChanged(toPosition)
    }
}
