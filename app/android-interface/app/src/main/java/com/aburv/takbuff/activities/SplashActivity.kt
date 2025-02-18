package com.aburv.takbuff.activities

import android.animation.AnimatorSet
import android.animation.ObjectAnimator
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.ActivityInfo
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.View
import android.view.animation.AnimationUtils
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityOptionsCompat
import com.aburv.takbuff.R
import com.aburv.takbuff.data.DeviceData
import com.aburv.takbuff.data.UserData
import com.aburv.takbuff.databinding.ActivitySplashBinding
import androidx.core.util.Pair as UtilPair


@SuppressLint("CustomSplashScreen")
class SplashActivity : AppCompatActivity() {

    companion object {
        const val SUB_TITLE_HIDE_DURATION = 2000L
        const val MOVE_UP_DURATION = 2000L
        const val WAIT_FOR_CALL_DURATION = 1000L

        const val FULL_OPACITY = 1.0f
        const val ZERO_OPACITY = 1.0f

        const val MOVE_UP_Y_COORDINATE = -500f
    }

    private val handler = Handler(Looper.getMainLooper())

    private val userData = UserData()
    private val deviceData = DeviceData()

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
        val hide = ObjectAnimator.ofFloat(appSubtitle, View.ALPHA, FULL_OPACITY, ZERO_OPACITY)
        hide.duration = SUB_TITLE_HIDE_DURATION
        val moveUp = ObjectAnimator.ofFloat(infoLayout, View.TRANSLATION_Y, MOVE_UP_Y_COORDINATE)
        moveUp.duration = MOVE_UP_DURATION

        try {
            deviceData.isDeviceRegistered(this)
            userData.getUserdata()

            appLogo.startAnimation(rotate)
        } catch (e: Exception) {
            appLogo.startAnimation(rotate)
            Log.e("App", "Error in Communicating server")
        }
        userData.data.observe(this) {
            handler.postDelayed(
                {
                    rotate.cancel()
                    AnimatorSet().apply {
                        this.play(moveUp).after(hide)
                    }.start()
                    handler.postDelayed(
                        { navigateMain() },
                        SUB_TITLE_HIDE_DURATION + MOVE_UP_DURATION
                    )
                },
                WAIT_FOR_CALL_DURATION
            )
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