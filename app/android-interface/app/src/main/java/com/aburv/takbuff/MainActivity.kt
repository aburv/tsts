package com.aburv.takbuff

import android.animation.Animator
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.view.ViewAnimationUtils
import android.view.inputmethod.InputMethodManager
import androidx.appcompat.app.AppCompatActivity
import com.aburv.takbuff.databinding.ActivityMainBinding


class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val searchIcon = binding.icSearch
        val searchLayout = binding.layoutSearch
        val closeIcon = binding.icBack
        val clearIcon = binding.icClear
        val searchText = binding.searchInputText
        val searchList = binding.listSearch

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

        clearIcon.setOnClickListener {
            searchText.text.clear()
        }

        searchText.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable) {}
            override fun beforeTextChanged(
                s: CharSequence,
                start: Int,
                count: Int,
                after: Int
            ) {
            }

            override fun onTextChanged(s: CharSequence, start: Int, before: Int, count: Int) {}
        })

    }
}