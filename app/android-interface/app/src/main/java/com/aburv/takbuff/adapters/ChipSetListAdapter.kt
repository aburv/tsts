package com.aburv.takbuff.adapters

import android.content.res.Resources
import android.graphics.Typeface
import android.util.Log
import android.util.TypedValue
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.annotation.ColorInt
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.aburv.takbuff.R


class ChipSetListAdapter(
    private val theme: Resources.Theme,
    private val type: ChipSet,
    private var dataSet: ArrayList<OptionData>,
    private val onChipClickEvent: OnChipClickEvent
) :
    RecyclerView.Adapter<ChipSetListAdapter.ViewHolder>() {
    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): ViewHolder {
        val view: View =
            LayoutInflater.from(parent.context).inflate(R.layout.item_chip, parent, false)
        val viewHolder = ViewHolder(theme, view)
        return viewHolder
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.content.text = dataSet[position].text
        holder.setOther()

        holder.itemView.setOnClickListener {
            onChipClickEvent.onChipSelect(type, holder, dataSet[position].id)
        }
    }

    override fun getItemCount() = dataSet.count()

    fun setData(data: ArrayList<OptionData>) {
        dataSet = data
        notifyDataSetChanged()
    }

    class ViewHolder(theme: Resources.Theme, itemView: View) :
        RecyclerView.ViewHolder(itemView) {
        val content: TextView = itemView.findViewById(R.id.content)
        private var isSelected = false

        @ColorInt
        var dark: Int? = null

        @ColorInt
        var bright: Int? = null

        private val typedValue = TypedValue()

        init {
            theme.resolveAttribute(R.attr.dark, typedValue, true)
            dark = typedValue.data

            theme.resolveAttribute(R.attr.bright, typedValue, true)
            bright = typedValue.data
        }

        fun toggleAndRenderUI() {
            if (!isSelected) {
                setSelected()
            } else {
                setOther()
            }
        }

        private fun setSelected() {
            isSelected = true
            content.setTextColor(bright!!)
            content.setTypeface(null, Typeface.BOLD)
            content.textSize = 14F
            content.background =
                ContextCompat.getDrawable(
                    itemView.context,
                    R.drawable.bg_chip_select
                )
        }

        fun setOther() {
            Log.i("Position chip", this.toString())
            isSelected = false
            content.setTextColor(dark!!)
            content.setTypeface(null, Typeface.NORMAL)
            content.textSize = 14F
            content.background =
                ContextCompat.getDrawable(
                    itemView.context,
                    R.drawable.bg_chip_unselect
                )
        }

    }

    interface OnChipClickEvent {
        fun onChipSelect(type: ChipSet, view: ViewHolder, id: String)
    }
}

enum class ChipSet {
    BLOOD_GROUP,
    GENDER,
    SHOE_SIZE,
    JERSEY_SIZE,
    POSITION
}

data class OptionData(val id: String, val text: String)
