package com.aburv.takbuff.activities

import android.animation.ObjectAnimator
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintSet
import androidx.core.app.ActivityOptionsCompat
import androidx.core.util.Pair
import androidx.fragment.app.Fragment
import androidx.lifecycle.lifecycleScope
import com.aburv.takbuff.R
import com.aburv.takbuff.data.Image
import com.aburv.takbuff.data.ImageViewUtil
import com.aburv.takbuff.data.PlayerFormData
import com.aburv.takbuff.data.PlayerFormDataResponse
import com.aburv.takbuff.data.PlayerActualDataResponse
import com.aburv.takbuff.data.PlayerService
import com.aburv.takbuff.data.Response
import com.aburv.takbuff.data.UserData
import com.aburv.takbuff.databinding.ActivityNewUserBinding
import com.aburv.takbuff.playerDetailFragments.PreviewFragment
import com.aburv.takbuff.playerDetailFragments.Step1Fragment
import com.aburv.takbuff.playerDetailFragments.Step2Fragment
import com.aburv.takbuff.playerDetailFragments.Step3Fragment
import com.aburv.takbuff.db.AppUser
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers.Main
import kotlinx.coroutines.Dispatchers.Default
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject

class NewUserActivity : AppCompatActivity() {

    companion object {
        private const val TAG = "App-NewUser"
        private const val FINAL_STEP = 4
    }

    private lateinit var binding: ActivityNewUserBinding
    private var user: AppUser? = null

    private lateinit var initialUserConstraints: ConstraintSet

    private var currentStep = 0
    private var isLoading = false
    private var corePlayerData: JSONObject? = null
    private var jerseyData: JSONObject? = null

    private var step2Fragment: Step2Fragment? = null
    private var step3Fragment: Step3Fragment? = null
    private var playerFormData: PlayerFormData? = null

    private var isPlayerPresent: Boolean = false

    private val cropResult = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == RESULT_OK) {
            result.data?.getStringExtra(ImageCropActivity.EXTRA_IMAGE_ID)?.let { imageId ->
                Image(this).load(imageId, "160") { data ->
                    binding.userDp.setImageBitmap(ImageViewUtil.getRoundedCornerBitmap(data, 60.0F))
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.i(TAG, "On Create")
        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_PAN)

        binding = ActivityNewUserBinding.inflate(layoutInflater)
        setContentView(binding.root)

        initialUserConstraints = ConstraintSet().also { it.clone(binding.layoutUser) }

        val userData = UserData(this)
        lifecycleScope.launch(Dispatchers.IO) {
            PlayerService(this@NewUserActivity).getFormData(object : PlayerFormDataResponse {
                override fun onData(value: PlayerFormData) {
                    playerFormData = value
                    step2Fragment?.setFormData(value)
                    step3Fragment?.setFormData(value)
                }

                override fun onError(value: String) {
                    Log.e(TAG, value)
                }
            })
        }
        lifecycleScope.launch(Dispatchers.IO) {
            PlayerService(this@NewUserActivity).getActualPlayer(object : PlayerActualDataResponse {
                override fun onData(value: String) {
                    isPlayerPresent = value.toBooleanStrict()
                }

                override fun onError(value: String) {
                    Log.e(TAG, value)
                }
            })
            PlayerService(this@NewUserActivity).getActualPlayerGear(object :
                PlayerActualDataResponse {
                override fun onData(value: String) {
                    jerseyData = JSONObject(value)
                }

                override fun onError(value: String) {
                    Log.e(TAG, value)
                }
            })
        }
        CoroutineScope(Main).launch {
            user = userData.getUser()
            setUserLayout()
        }

        binding.button.setOnClickListener {
            Log.i(TAG, "Action Button pressed")

            if (!binding.button.isEnabled || isLoading) return@setOnClickListener
            when (currentStep) {
                2 -> submitCorePlayerData()
                3 -> submitJerseyData()
                4 -> {
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
                }
                else -> {
                    currentStep += 1
                    updateFragment()
                }
            }
        }
        updateFragment()

        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {
                override fun handleOnBackPressed() {
                    Log.i(TAG, "On Back pressed")
                    if (isFirstStep()) {
                        finishAffinity()
                    } else {
                        currentStep -= 1
                        if (isFirstStep()) {
                            resetUserLayout()
                        }
                        updateFragment()
                    }
                }
            }
        )

        binding.userDp.setOnClickListener {
            if (currentStep == 0) {
                navigateCrop()
            }
        }
        binding.editDp.bringToFront()
    }

    override fun dispatchTouchEvent(event: MotionEvent): Boolean {
        // If the EditText is focused and the user touches outside
        val v = currentFocus
        if (v is EditText) {
            if (event.action == MotionEvent.ACTION_DOWN) {
                // If touch is outside the EditText, remove focus
                v.clearFocus()

                // Hide the soft keyboard
                val imm = getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager
                imm.hideSoftInputFromWindow(v.windowToken, 0)
            }
        }
        return super.dispatchTouchEvent(event)
    }

    private fun updateFragment() {
        Log.i(TAG, "Update fragment")

        when (currentStep) {
            0 -> binding.steps.visibility = View.GONE
            1 -> {
                startAnimation()
                loadFragment(Step1Fragment())
            }

            2 -> {
                if (isPlayerPresent) {
                    currentStep = 3
                    updateFragment()
                    return
                }
                step2Fragment = Step2Fragment(this, playerFormData).also {
                    it.setOnFormChanged { updateButtonState() }
                    loadFragment(it)
                }
            }

            3 -> {
                if (jerseyData!!.length() != 0) {
                    currentStep = 4
                    updateFragment()
                    return
                }
                step3Fragment = Step3Fragment(this, playerFormData).also {
                    it.setOnFormChanged { updateButtonState() }
                    loadFragment(it)
                }
            }

            else -> loadFragment(PreviewFragment(this, jerseyData))
        }
        binding.button.setImageResource(
            if (isFinalStep()) R.drawable.ic_tick else R.drawable.ic_right_arrow
        )
        updateButtonState()
    }

    private fun startAnimation() {
        val density = resources.displayMetrics.density
        val margin = (16 * density).toInt()
        val imageSize = (80 * density).toInt()
        val transition = android.transition.TransitionSet()
            .addTransition(android.transition.ChangeBounds())
            .setDuration(1000)

        binding.steps.visibility = View.VISIBLE
        binding.editDp.visibility = View.GONE
        binding.steps.alpha = 0f
        android.transition.TransitionManager.beginDelayedTransition(
            binding.layoutContent,
            transition
        )

        val endConstraints = ConstraintSet().also { it.clone(binding.layoutUser) }
        endConstraints.constrainWidth(binding.userDp.id, imageSize)
        endConstraints.constrainHeight(binding.userDp.id, imageSize)
        endConstraints.clear(binding.userDp.id, ConstraintSet.END)
        endConstraints.connect(
            binding.userDp.id,
            ConstraintSet.START,
            ConstraintSet.PARENT_ID,
            ConstraintSet.START,
            margin
        )
        endConstraints.clear(binding.userDp.id, ConstraintSet.BOTTOM)
        endConstraints.connect(
            binding.userDp.id,
            ConstraintSet.TOP,
            ConstraintSet.PARENT_ID,
            ConstraintSet.TOP,
            margin
        )

        endConstraints.clear(binding.userName.id, ConstraintSet.START)
        endConstraints.clear(binding.userName.id, ConstraintSet.END)
        endConstraints.connect(
            binding.userName.id,
            ConstraintSet.START,
            binding.userDp.id,
            ConstraintSet.END,
            margin
        )
        endConstraints.clear(binding.userName.id, ConstraintSet.BOTTOM)
        endConstraints.connect(
            binding.userName.id,
            ConstraintSet.TOP,
            ConstraintSet.PARENT_ID,
            ConstraintSet.TOP,
            margin
        )

        endConstraints.clear(binding.userEmail.id, ConstraintSet.START)
        endConstraints.clear(binding.userEmail.id, ConstraintSet.END)
        endConstraints.connect(
            binding.userEmail.id,
            ConstraintSet.START,
            binding.userName.id,
            ConstraintSet.START
        )
        endConstraints.clear(binding.editDp.id, ConstraintSet.END)
        endConstraints.clear(binding.editDp.id, ConstraintSet.BOTTOM)
        endConstraints.connect(
            binding.editDp.id,
            ConstraintSet.END,
            binding.userDp.id,
            ConstraintSet.END
        )
        endConstraints.connect(
            binding.editDp.id,
            ConstraintSet.BOTTOM,
            binding.userDp.id,
            ConstraintSet.BOTTOM
        )
        endConstraints.applyTo(binding.layoutUser)

        ObjectAnimator.ofFloat(binding.steps, View.ALPHA, 0f, 1f).apply {
            duration = 1000
            start()
        }
    }

    private fun resetUserLayout() {
        initialUserConstraints.applyTo(binding.layoutUser)
        binding.editDp.visibility = View.VISIBLE
        binding.userDp.layoutParams.width = (180 * resources.displayMetrics.density).toInt()
        binding.userDp.layoutParams.height = (180 * resources.displayMetrics.density).toInt()
        binding.userDp.translationX = 0f
        binding.userDp.translationY = 0f
        binding.userName.translationX = 0f
        binding.userName.translationY = 0f
        binding.userEmail.translationX = 0f
        binding.userEmail.translationY = 0f
        binding.steps.alpha = 1f
    }

    private fun loadFragment(fragment: Fragment) {
        supportFragmentManager
            .beginTransaction()
            .replace(R.id.steps, fragment)
            .commit()
    }

    private fun updateButtonState() {
        if (isLoading) return
        val enabled = when (currentStep) {
            2 -> step2Fragment?.view != null && step2Fragment?.isValid() == true
            3 -> step3Fragment?.view != null && step3Fragment?.isValid() == true
            else -> true
        }
        binding.button.isEnabled = enabled
        binding.button.alpha = if (enabled) 1f else 0.45f
    }

    private fun submitCorePlayerData() {
        val data = step2Fragment?.takeIf { it.isValid() }?.collectData() ?: run {
            updateButtonState()
            return
        }
        isLoading = true
        binding.button.isEnabled = false
        binding.button.alpha = 1f
        binding.button.setImageResource(R.drawable.ic_loading_spinner)
        binding.button.startAnimation(
            android.view.animation.AnimationUtils.loadAnimation(
                this,
                R.anim.rotate
            )
        )
        lifecycleScope.launch(Dispatchers.IO) {
            PlayerService(this@NewUserActivity).create(data, object : Response {
                override fun onData(value: String) {
                    finishLoading()
                    corePlayerData = data
                    currentStep += 1
                    updateFragment()
                }

                override fun onError(value: String) {
                    finishLoading()
                    Toast.makeText(this@NewUserActivity, value, Toast.LENGTH_LONG).show()
                }
            })
        }
    }

    private fun submitJerseyData() {
        val data = step3Fragment?.takeIf { it.isValid() }?.collectData() ?: run {
            updateButtonState()
            return
        }
        isLoading = true
        binding.button.isEnabled = false
        binding.button.alpha = 1f
        binding.button.setImageResource(R.drawable.ic_loading_spinner)
        binding.button.startAnimation(
            android.view.animation.AnimationUtils.loadAnimation(
                this,
                R.anim.rotate
            )
        )
        lifecycleScope.launch(Dispatchers.IO) {
            PlayerService(this@NewUserActivity).updateJersey(data, object : Response {
                override fun onData(value: String) {
                    finishLoading()
                    jerseyData = data
                    currentStep += 1
                    updateFragment()
                }

                override fun onError(value: String) {
                    finishLoading()
                    Toast.makeText(this@NewUserActivity, value, Toast.LENGTH_LONG).show()
                }
            })
        }
    }

    private fun isFirstStep() = currentStep == 0

    private fun isFinalStep() = currentStep == FINAL_STEP

    private fun setUserLayout() {
        Log.i(TAG, "Set Profile data")

        if (user != null) {
            val userName = user!!.name
            binding.userName.text = userName
            binding.userName.textSize = if (userName.length > 15) 20.0F else 25.0F
            val userMail = user!!.email
            binding.userEmail.text = userMail
            binding.userEmail.textSize = if (userMail.length > 20) 16.0F else 20.0F
            if (user!!.dp == "") {
                binding.userDp.setImageResource(R.drawable.ic_person)
            } else {
                Image(this).load(user!!.dp, "160") { data ->
                    val roundedImageData = ImageViewUtil.getRoundedCornerBitmap(data, 60.0F)
                    binding.userDp.setImageBitmap(roundedImageData)
                }
            }
        }
    }

    private fun finishLoading() {
        isLoading = false
        binding.button.clearAnimation()
        updateButtonState()
    }

    private fun navigateMain() {
        Log.i(TAG, "Navigating to Main")
        val intent = Intent(this, MainActivity::class.java)
        val p1: Pair<View, String> = Pair.create(binding.userDp as View, "dp")
        val p2: Pair<View, String> = Pair.create(binding.appIcon as View, "logo")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@NewUserActivity, p1, p2)
        startActivity(intent, options.toBundle())
    }

    private fun navigateCrop() {
        val intent = Intent(this, ImageCropActivity::class.java)
        val p1: Pair<View, String> = Pair.create(binding.userDp as View, "dp")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@NewUserActivity, p1)
        cropResult.launch(intent, options)
    }
}