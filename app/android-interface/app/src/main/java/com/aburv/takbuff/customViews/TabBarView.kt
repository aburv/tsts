package com.aburv.takbuff.customViews

import android.animation.ObjectAnimator
import android.content.Context
import android.graphics.Typeface
import android.os.Handler
import android.os.Looper
import android.util.AttributeSet
import android.util.TypedValue
import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.widget.LinearLayout
import android.widget.RelativeLayout
import android.widget.TextView
import androidx.annotation.ColorInt
import androidx.core.animation.doOnEnd
import androidx.viewpager.widget.ViewPager
import com.aburv.takbuff.R
import com.aburv.takbuff.databinding.LayoutTabBarBinding

class TabBarView(context: Context?, attrs: AttributeSet?) :
    RelativeLayout(context, attrs) {

    private var binding: LayoutTabBarBinding =
        LayoutTabBarBinding.inflate(LayoutInflater.from(context), this, true)
    
    private var listTabName: List<String> = arrayListOf()
    private var listTabTv: List<TextView> = arrayListOf()
    private var isAnimating = false
    private var onTabSelectedListener: ((Int) -> Unit)? = null

    private val typedValue = TypedValue()
    val theme = context!!.theme

    @ColorInt
    var dark: Int? = null

    @ColorInt
    var bright: Int? = null

    init {
        theme.resolveAttribute(R.attr.dark, typedValue, true)
        dark = typedValue.data

        theme.resolveAttribute(R.attr.bright, typedValue, true)
        bright = typedValue.data
    }

    fun attachTo(viewPager: ViewPager) {
        onTabSelectedListener = {
            viewPager.setCurrentItem(it, true)
        }
        viewPager.addOnPageChangeListener(object : ViewPager.OnPageChangeListener {
            override fun onPageScrolled(
                position: Int,
                positionOffset: Float,
                positionOffsetPixels: Int
            ) {}

            override fun onPageSelected(position: Int) {
                if (!isAnimating) {
                    onTabSelected(position)
                }
            }

            override fun onPageScrollStateChanged(state: Int) {}
        })
    }

    fun setTitles(tabTitles: List<String>) {
        listTabName = tabTitles
        setupUI()
    }

    private fun setupUI() {
        listTabTv = listTabName.mapIndexed { index, tabName ->
            initTabTv(tabName, index)
        }

        binding.viewTabsWrapper.apply {
            weightSum = listTabTv.size.toFloat()
            listTabTv.forEach {
                this.addView(it)
            }
        }

        binding.viewIndicatorWrapper.apply {
            weightSum = listTabTv.size.toFloat()
        }
    }

    private fun initTabTv(tabName: String, index: Int) = TextView(context).apply {
        text = tabName
        layoutParams = LinearLayout.LayoutParams(
            0,
            LayoutParams.MATCH_PARENT,
            1f
        )
        gravity = Gravity.CENTER

        if (index == 0) {
            setSelected(this)
        } else {
            setOther(this)
        }
        setOnClickListener {
            onTabSelected(index)
        }
    }

    private fun setSelected(tv: TextView) {
        tv.setTextColor(bright!!)
        tv.setTypeface(null, Typeface.BOLD)
        tv.textSize = 16F
    }

    private fun setOther(tv: TextView) {
        tv.setTextColor(dark!!)
        tv.setTypeface(null, Typeface.NORMAL)
        tv.textSize = 14F
    }

    private fun onTabSelected(index: Int) {
        listTabTv.mapIndexed { tvIndex, tabTv ->
            if (index == tvIndex) {
                setSelected(tabTv)
            } else {
                setOther(tabTv)
            }
        }

        Handler(Looper.getMainLooper()).post {
            ObjectAnimator.ofFloat(
                binding.viewIndicator,
                View.TRANSLATION_X,
                binding.viewIndicator.x,
                listTabTv[index].x
            ).apply {
                duration = 300
                onTabSelectedListener?.invoke(index)
                isAnimating = true
                start()
                doOnEnd {
                    isAnimating = false
                }
            }
        }
    }
}