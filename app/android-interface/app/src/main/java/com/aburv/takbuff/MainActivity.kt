package com.aburv.takbuff

import android.animation.Animator
import android.content.pm.ActivityInfo
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.view.ViewAnimationUtils
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.view.inputmethod.InputMethodManager
import android.widget.ImageView
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintLayout
import com.aburv.takbuff.databinding.ActivityMainBinding
import com.aburv.takbuff.mainFragments.DashboardFragment


class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    private var clearIcon: ImageView? = null
    private var loaderLayout: ConstraintLayout? = null
    private var loadingAppLogo: ImageView? = null

    private var searchingvalue: String = ""

    private var loadingRotate: Animation? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()

        requestedOrientation = if (resources.getBoolean(R.bool.isTablet)) {
            ActivityInfo.SCREEN_ORIENTATION_SENSOR
        } else {
            ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        }

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        if (savedInstanceState == null) {
            supportFragmentManager
                .beginTransaction()
                .add(R.id.container, DashboardFragment())
                .commit()
        }

        clearIcon = binding.icClear
        loaderLayout = binding.loadingLayout
        loadingAppLogo = binding.loadingAppIcon

        val searchIcon = binding.icSearch
        val searchLayout = binding.layoutSearch
        val closeIcon = binding.icBack
        val searchText = binding.searchInputText
        val searchList = binding.listSearch

        loadingRotate = AnimationUtils.loadAnimation(this, R.anim.rotate)
        loadingRotate!!.fillAfter = true
        setLoadingOff()

        searchIcon.setOnClickListener {
            searchLayout.visibility = View.VISIBLE
            searchList.visibility = View.VISIBLE
            val circularReveal = ViewAnimationUtils.createCircularReveal(
                searchLayout,
                (searchIcon.right + searchIcon.left) / 2,
                (searchIcon.top + searchIcon.bottom) / 2,
                0f, searchIcon.width.toFloat()
            )
            circularReveal.duration = 300
            circularReveal.start()

            val inputMethodManager = getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager
            inputMethodManager.toggleSoftInputFromWindow(
                searchText.applicationWindowToken,
                InputMethodManager.SHOW_IMPLICIT, 0
            )
        }

        closeIcon.setOnClickListener {
            searchText.text.clear()
            val imm = getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager
            imm.hideSoftInputFromWindow(searchText.windowToken, 0)

            val circularConceal = ViewAnimationUtils.createCircularReveal(
                searchIcon,
                (searchIcon.right + searchIcon.left) / 2,
                (searchIcon.top + searchIcon.bottom) / 2,
                searchIcon.width.toFloat(), 0f
            )


            circularConceal.duration = 300
            circularConceal.start()
            circularConceal.addListener(object : Animator.AnimatorListener {
                override fun onAnimationRepeat(animation: Animator) = Unit
                override fun onAnimationCancel(animation: Animator) = Unit
                override fun onAnimationStart(animation: Animator) = Unit
                override fun onAnimationEnd(animation: Animator) {
                    searchLayout.visibility = View.GONE
                    searchList.visibility = View.GONE
                    circularConceal.removeAllListeners()
                }
            })
        }

        clearIcon!!.setOnClickListener {
            searchText.text.clear()
        }

        updateSearchCloseIcon()

        searchText.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable) {
                searchingvalue = s.toString()
                updateSearchCloseIcon()
            }

            override fun beforeTextChanged(
                s: CharSequence,
                start: Int,
                count: Int,
                after: Int
            ) {
            }

            override fun onTextChanged(s: CharSequence, start: Int, before: Int, count: Int) {}
        })

        onBackPressedDispatcher.addCallback(this,
            object : OnBackPressedCallback(true) {
                override fun handleOnBackPressed() {
                    finishAffinity()
                }
            })
    }

    private fun setLoadingOn() {
        loaderLayout!!.visibility = View.VISIBLE
        loadingAppLogo!!.startAnimation(loadingRotate!!)
    }

    private fun setLoadingOff() {
        loaderLayout!!.visibility = View.GONE
        loadingRotate!!.cancel()
    }

    private fun updateSearchCloseIcon() {
        if (searchingvalue.isNotBlank()) {
            clearIcon!!.visibility = View.VISIBLE
        } else {
            clearIcon!!.visibility = View.INVISIBLE
        }
    }
}