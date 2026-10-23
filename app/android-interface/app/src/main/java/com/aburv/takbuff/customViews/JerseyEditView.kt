package com.aburv.takbuff.customViews

import android.content.Context
import android.util.AttributeSet
import android.util.TypedValue
import android.view.LayoutInflater
import android.widget.EditText
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.view.doOnLayout
import com.aburv.takbuff.R

class JerseyEditView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : ConstraintLayout(context, attrs, defStyleAttr) {

    private var nameInput: EditText
    private var numberInput: EditText

    // Original design dimensions
    private val baseHeightPx =
        300f * resources.displayMetrics.density

    private val baseWidthPx =
        350f * resources.displayMetrics.density

    private var baseNameTextSizePx = 0f
    private var baseNumberTextSizePx = 0f

    init {
        LayoutInflater.from(context).inflate(
            R.layout.view_jersey_edit,
            this,
            true
        )

        nameInput = findViewById(R.id.jersey_name)
        numberInput = findViewById(R.id.jersey_number)

        // Center text and cursor horizontally
        nameInput.gravity =
            android.view.Gravity.CENTER

        numberInput.gravity =
            android.view.Gravity.CENTER

        nameInput.textAlignment =
            android.view.View.TEXT_ALIGNMENT_CENTER

        numberInput.textAlignment =
            android.view.View.TEXT_ALIGNMENT_CENTER

        // Save original font sizes before scaling
        baseNameTextSizePx = nameInput.textSize
        baseNumberTextSizePx = numberInput.textSize

        // Apply scaling after the initial layout
        doOnLayout {
            applyJerseyScaling()
        }
    }

    override fun onSizeChanged(
        w: Int,
        h: Int,
        oldw: Int,
        oldh: Int
    ) {
        super.onSizeChanged(w, h, oldw, oldh)

        if (w <= 0 || h <= 0) return

        post {
            applyJerseyScaling()
        }
    }

    private fun applyJerseyScaling() {
        val actualHeight = height

        if (actualHeight <= 0 || baseHeightPx <= 0f) {
            return
        }

        // Scale proportionally from the original 300dp height
        val scale = actualHeight / baseHeightPx
        val density = resources.displayMetrics.density

        // Scale name position and height
        val nameParams =
            nameInput.layoutParams as LayoutParams

        nameParams.topMargin =
            (65f * density * scale).toInt()

        nameParams.height =
            (40f * density * scale).toInt()

        nameInput.layoutParams = nameParams

        // Scale number spacing
        val numberParams =
            numberInput.layoutParams as LayoutParams

        numberParams.topMargin =
            (5f * density * scale).toInt()

        numberInput.layoutParams = numberParams

        // Scale font sizes
        nameInput.setTextSize(
            TypedValue.COMPLEX_UNIT_PX,
            baseNameTextSizePx * scale
        )

        numberInput.setTextSize(
            TypedValue.COMPLEX_UNIT_PX,
            baseNumberTextSizePx * scale
        )
    }

    fun setJerseyName(name: String) {
        nameInput.setText(name)
    }

    fun setJerseyNumber(number: String) {
        numberInput.setText(number)
    }

    fun getJerseyName(): String =
        nameInput.text.toString().trim()

    fun getJerseyNumber(): String =
        numberInput.text.toString().trim()

    fun setJerseyBackground(drawableRes: Int) {
        setBackgroundResource(drawableRes)
    }
}
