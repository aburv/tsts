package com.aburv.takbuff.activities

import android.animation.AnimatorSet
import android.animation.ObjectAnimator
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.ActivityInfo
import android.os.Bundle
import android.view.View
import android.view.animation.AnimationUtils
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityOptionsCompat
import com.aburv.takbuff.R
import com.aburv.takbuff.databinding.ActivitySplashBinding
import androidx.core.util.Pair as UtilPair


@SuppressLint("CustomSplashScreen")
class SplashActivity : AppCompatActivity() {

    private lateinit var binding: ActivitySplashBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()

        requestedOrientation = if (resources.getBoolean(R.bool.isTablet)) {
            ActivityInfo.SCREEN_ORIENTATION_SENSOR
        } else {
            ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        }

        binding = ActivitySplashBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val infoLayout = binding.layoutAppInfo
        val appSubtitle = binding.appSubtitle
        val appLogo = binding.appIcon

        val rotate = AnimationUtils.loadAnimation(this, R.anim.rotate)
        rotate.fillAfter = true
        val hide = ObjectAnimator.ofFloat(appSubtitle, View.ALPHA, 1.0f, 0.0f)
        hide.duration = 3000
        val moveUp = ObjectAnimator.ofFloat(infoLayout, View.TRANSLATION_Y, -500f)
        moveUp.duration = 2000

        appLogo.startAnimation(rotate)

        AnimatorSet().apply {
            this.play(moveUp).after(hide)
        }.start()

        appLogo.setOnClickListener {
            navigateMain()
        }
    }

    private fun navigateMain() {
        val intent = Intent(this, MainActivity::class.java)
        val p1: UtilPair<View, String> = UtilPair.create(binding.appIcon as View, "logo")
        val p2: UtilPair<View, String> = UtilPair.create(binding.appName as View, "name")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@SplashActivity, p1, p2)
        startActivity(intent, options.toBundle())
    }
}