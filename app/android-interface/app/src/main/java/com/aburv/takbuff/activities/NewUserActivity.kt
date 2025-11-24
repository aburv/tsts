package com.aburv.takbuff.activities

import android.animation.Animator
import android.animation.AnimatorListenerAdapter
import android.animation.AnimatorSet
import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.content.Intent
import android.content.res.Resources
import android.os.Bundle
import android.util.Log
import android.view.View
import android.view.animation.LinearInterpolator
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.app.ActivityOptionsCompat
import androidx.core.util.Pair
import androidx.fragment.app.Fragment
import com.aburv.takbuff.R
import com.aburv.takbuff.data.Image
import com.aburv.takbuff.data.ImageViewUtil
import com.aburv.takbuff.data.Response
import com.aburv.takbuff.data.UserData
import com.aburv.takbuff.databinding.ActivityNewUserBinding
import com.aburv.takbuff.db.AppUser
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers.Default
import kotlinx.coroutines.Dispatchers.Main
import kotlinx.coroutines.launch

class NewUserActivity : AppCompatActivity() {

    companion object {
        private const val TAG = "App-NewUser"
        private const val FINAL_STEP = 1
    }

    private lateinit var binding: ActivityNewUserBinding
    private var user: AppUser? = null

    private var logo: ImageView? = null
    private var dp: ImageView? = null
    private var email: TextView? = null
    private var name: TextView? = null

    private var currentStep = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.i(TAG, "On Create")
        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()

        binding = ActivityNewUserBinding.inflate(layoutInflater)
        setContentView(binding.root)

        name = binding.userName
        email = binding.userEmail
        dp = binding.userDp
        logo = binding.appIcon

        val userData = UserData(this)
        CoroutineScope(Main).launch {
            user = userData.getUser()
            setUserLayout()
        }

        binding.button.setOnClickListener {
            Log.i(TAG, "Action Button pressed")

            if (isFinalStep()) {
                CoroutineScope(Default).launch {
                    userData.setOnBoardingDone(object : Response {
                        override fun onData(value: String) {
                            navigateMain()
                        }

                        override fun onError(value: String) {
                            Log.e(TAG, value)
                        }
                    })
                }
            } else {
                currentStep += 1
                updateFragment()
            }
        }
        updateFragment()
    }

    private fun updateFragment() {
        Log.i(TAG, "Update fragment")

        when (currentStep) {
            0 -> binding.steps.visibility = View.GONE
            1 -> {
                startAnimation()
            }
        }
        if (isFinalStep()) {
            binding.button.setImageResource(R.drawable.ic_tick)
        }
    }

    private fun startAnimation() {
        val userImageTranslateX = ObjectAnimator.ofFloat(
            binding.userDp,
            "translationX",
            0f,
            -380f
        )
        val userImageTranslateY = ObjectAnimator.ofFloat(
            binding.userDp,
            "translationY",
            0f,
            20f
        )

        val userNameTranslateX = ObjectAnimator.ofFloat(
            binding.userName,
            "translationX",
            0f,
            -100f
        )
        val userNameTranslateY = ObjectAnimator.ofFloat(
            binding.userName,
            "translationY",
            0f,
            -175f
        )

        val userNameTextSize = ObjectAnimator.ofFloat(
            binding.userName,
            "textSize",
            24f,
            20f
        )

        val userEmailTranslateX = ObjectAnimator.ofFloat(
            binding.userEmail,
            "translationX",
            0f,
            0f
        )
        val userEmailTranslateY = ObjectAnimator.ofFloat(
            binding.userEmail,
            "translationY",
            0f,
            -175f
        )

        val userEmailTextSize = ObjectAnimator.ofFloat(
            binding.userEmail,
            "textSize",
            20f,
            16f
        )

        val animator = ObjectAnimator.ofFloat(binding.steps, "alpha", 0f, 1f)

        animator.duration = 1000

        animator.addListener(object : AnimatorListenerAdapter() {
            override fun onAnimationEnd(animation: Animator) {
                binding.steps.visibility = View.VISIBLE
            }

            override fun onAnimationStart(animation: Animator) {
                binding.steps.visibility = View.VISIBLE
            }
        })

        val animatorSet = AnimatorSet()
        animatorSet.playTogether(
            userImageTranslateX,
            userImageTranslateY,
            userNameTranslateX,
            userNameTranslateY,
            userNameTextSize,
            userEmailTranslateX,
            userEmailTranslateY,
            userEmailTextSize,
            animator
        )

        animatorSet.duration = 1000

        animatorSet.start()
        animateWidthAndHeight()
    }

    private fun animateWidthAndHeight() {
        val widthAnimator =
            ValueAnimator.ofInt(180.iDp2Px, 80.iDp2Px)
        widthAnimator.duration = 1000
        widthAnimator.interpolator = LinearInterpolator()

        val heightAnimator =
            ValueAnimator.ofInt(180.iDp2Px, 80.iDp2Px)
        heightAnimator.duration = 1000
        heightAnimator.interpolator = LinearInterpolator()

                widthAnimator.addUpdateListener { animation: ValueAnimator ->
            val width = animation.animatedValue as Int
            updateImageViewSize(width, binding.userDp.layoutParams.height)
        }

        heightAnimator.addUpdateListener { animation: ValueAnimator ->
            val height = animation.animatedValue as Int
            updateImageViewSize(binding.userDp.layoutParams.width, height)
        }

        widthAnimator.start()
        heightAnimator.start()
    }

    private fun updateImageViewSize(width: Int, height: Int) {
        val layoutParams = binding.userDp.layoutParams

        layoutParams.width = width
        layoutParams.height = height

        binding.userDp.layoutParams = layoutParams
    }

    private fun isFinalStep() = currentStep == FINAL_STEP

    private fun setUserLayout() {
        Log.i(TAG, "Set Profile data")

        if (user != null) {
            name!!.text = user!!.name
            email!!.text = user!!.email
            if (user!!.dp == "") {
                dp!!.setImageResource(R.drawable.ic_person)
            } else {
                Image(this).load(user!!.dp, "160") { data ->
                    val roundedImageData = ImageViewUtil.getRoundedCornerBitmap(data, 60.0F)
                    dp!!.setImageBitmap(roundedImageData)
                }
            }
        }
    }

    private fun navigateMain() {
        Log.i(TAG, "Navigating to Main")
        val intent = Intent(this, MainActivity::class.java)
        val p1: Pair<View, String> = Pair.create(dp as View, "dp")
        val p2: Pair<View, String> = Pair.create(logo as View, "logo")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@NewUserActivity, p1, p2)
        startActivity(intent, options.toBundle())
    }
}

val Int.iDp2Px: Int get() = (this * Resources.getSystem().displayMetrics.density).toInt()
