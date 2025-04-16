package com.aburv.takbuff.activities

import android.animation.AnimatorSet
import android.animation.ObjectAnimator
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.ActivityInfo
import android.location.Location
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.app.ActivityOptionsCompat
import com.aburv.takbuff.R
import com.aburv.takbuff.data.Auth
import com.aburv.takbuff.data.AuthUtil
import com.aburv.takbuff.data.DeviceData
import com.aburv.takbuff.data.LocationData
import com.aburv.takbuff.data.LoginResponse
import com.aburv.takbuff.data.UserData
import com.aburv.takbuff.databinding.ActivitySplashBinding
import com.aburv.takbuff.db.UserTokenDB
import com.aburv.takbuff.services.GAuthService
import com.aburv.takbuff.services.GoogleAuthResponse
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.google.android.material.bottomsheet.BottomSheetDialog
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import androidx.core.util.Pair as UtilPair


@SuppressLint("CustomSplashScreen")
class SplashActivity : AppCompatActivity() {

    companion object {
        private const val TAG = "App-Splash"
        private const val SUB_TITLE_HIDE_DURATION = 2000L
        private const val MOVE_UP_DURATION = 2000L
        private const val WAIT_FOR_CALL_DURATION = 1000L

        private const val FULL_OPACITY = 1.0f
        private const val ZERO_OPACITY = 0.0f

        private const val MOVE_UP_Y_COORDINATE = -500f

        private val HANDLER = Handler(Looper.getMainLooper())
    }

    private lateinit var binding: ActivitySplashBinding

    private var locationData: LocationData? = null

    private var userData: UserData? = null
    private var authData: Auth? = null
    private var deviceData: DeviceData? = null

    private var hasUser: Boolean = false

    private var googleErrorView: View? = null
    private var errorDialog: BottomSheetDialog? = null

    private var errorText: TextView? = null
    private var errorLayout: ConstraintLayout? = null

    private var userSignInLayout: ConstraintLayout? = null

    private var rotate: Animation? = null
    private var moveUp: ObjectAnimator? = null
    private var hide: ObjectAnimator? = null

    private var location: Location? = null

    private var isOnError = false

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.i(TAG, "On Create")

        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()

        requestedOrientation = if (resources.getBoolean(R.bool.isTablet)) {
            ActivityInfo.SCREEN_ORIENTATION_SENSOR
        } else {
            ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        }

        binding = ActivitySplashBinding.inflate(layoutInflater)
        setContentView(binding.root)

        locationData = LocationData(this)
        userData = UserData(this)
        authData = Auth(this)
        deviceData = DeviceData(this)

        val infoLayout = binding.layoutAppInfo
        val appSubtitle = binding.appSubtitle
        val appLogo = binding.appIcon

        userSignInLayout = binding.layoutUser
        val signInButton: ConstraintLayout = binding.buttonGoogleSignIn
        val skipButton = binding.buttonSkip

        errorLayout = binding.layoutError
        errorText = binding.textErrorMessage
        val retryButton = binding.buttonRetry

        errorDialog = BottomSheetDialog(this, R.style.AppBottomSheetDialogTheme)

        googleErrorView = LayoutInflater.from(this)
            .inflate(R.layout.layout_bottom_error_dialog, null)
        errorDialog!!.setContentView(googleErrorView!!)

        rotate = AnimationUtils.loadAnimation(this, R.anim.rotate)
        rotate!!.fillAfter = true
        hide = ObjectAnimator.ofFloat(appSubtitle, View.ALPHA, FULL_OPACITY, ZERO_OPACITY)
        hide!!.duration = SUB_TITLE_HIDE_DURATION
        moveUp = ObjectAnimator.ofFloat(infoLayout, View.TRANSLATION_Y, MOVE_UP_Y_COORDINATE)
        moveUp!!.duration = MOVE_UP_DURATION

        errorLayout!!.visibility = View.GONE
        appLogo.startAnimation(rotate)

        deviceData!!.isDeviceRegistered()

        CoroutineScope(Dispatchers.Default).launch {
            doInit()
        }

        signInButton.setOnClickListener {
            Log.i(TAG, "Sign in Button pressed")
            GAuthService(this).auth(object : GoogleAuthResponse {
                override fun onUser(googleUser: GoogleIdTokenCredential) {
                    Log.i(TAG, "On Google User $googleUser")
                    CoroutineScope(Dispatchers.Default).launch {
                        appLogin(googleUser)
                    }
                }

                override fun onError(message: String) {
                    Log.i(TAG, "On Google User Error $message")
                    onGoogleErrorDialog(message)
                }

            })
        }

        skipButton.setOnClickListener {
            Log.i(TAG, "Skip Button pressed")
            navigateMain()
        }

        retryButton.setOnClickListener {
            Log.i(TAG, "Retry Button pressed")
            isOnError = false
            errorLayout!!.visibility = View.GONE
            appLogo.startAnimation(rotate)
            CoroutineScope(Dispatchers.Default).launch {
                doInit()
            }
        }

        userData!!.data.observe(this) {
            Log.i(TAG, "User Data")
            proceedAfterLoading()
        }

        userData!!.error.observe(this) { errorMessage ->
            Log.i(TAG, "User Data On Error $errorMessage")
            onError(errorMessage)
        }
    }

    private fun getLocation() {
        Log.i(TAG, "Get Location")

        if (locationData!!.isAvailable()) {
            location = locationData!!.getCurrentLocation()
            if (location != null) {
                Log.i(TAG, "${location!!.latitude} , ${location!!.longitude}")
            } else {
                onError("Unable to get location data")
            }
        } else {
            onError("Turn Location ON")
        }
    }

    private fun proceedAfterLoading() {
        Log.i(TAG, "Proceed after loading")
        if (!isOnError) {
            HANDLER.postDelayed(
                {
                    rotate!!.cancel()
                    AnimatorSet().apply {
                        this.play(moveUp!!).after(hide!!)
                    }.start()

                    HANDLER.postDelayed(
                        {
                            if (hasUser) {
                                navigateMain()
                            } else {
                                userSignInLayout!!.visibility = View.VISIBLE
                            }
                        }, SUB_TITLE_HIDE_DURATION + MOVE_UP_DURATION
                    )
                }, WAIT_FOR_CALL_DURATION
            )
        }
    }

    private suspend fun doInit() {
        Log.i(TAG, "Do Init")
        try {
            locationData!!.requestPermission()
            locationData!!.setProvider()
            try {
                getLocation()
            } catch (e: SecurityException) {
                Log.i(TAG, "Location permission error $e")
            }
            Log.i(TAG, "Device Registration")
            deviceData!!.isDeviceRegistered()
            Log.i(TAG, "Check for user")
            hasUser = UserTokenDB(this).getUserToken().isNotEmpty()
            Log.i(TAG, "User Status $hasUser")
            if (hasUser) {
                Log.i(TAG, "Refresh User token")
                authData!!.refreshToken()
                Log.i(TAG, "Get User data")
                userData!!.getUserdata()
            } else {
                proceedAfterLoading()
            }
        } catch (e: Exception) {
            Log.i(TAG, "Init calls: Unable to connect to server $e")
            onError("Unexpected error connecting server")
        }
    }

    private suspend fun appLogin(googleUser: GoogleIdTokenCredential) {
        Log.i(TAG, "Login api Start")
        val locationData: kotlin.Pair<String, String>? = if (location != null)
            kotlin.Pair(location!!.latitude.toString(), location!!.longitude.toString())
        else null

        authData!!.login(
            googleUser.displayName!!,
            googleUser.profilePictureUri.toString(),
            googleUser.id,
            AuthUtil.parseToken(googleUser.idToken, "sub")!!,
            locationData,
            object : LoginResponse {
                override fun onNewUser() {
                    Log.i(TAG, "on new user")
                    navigateNewUser()
                }

                override fun onExistingUser() {
                    Log.i(TAG, "on existing user")
                    navigateMain()
                }

                override fun onError(message: String) {
                    Log.i(TAG, "Error on user: $message")
                    onError(message)
                }
            })
    }

    private fun onGoogleErrorDialog(message: String) {
        Log.i(TAG, "Google Error Dialog Visible on $message")
        HANDLER.postDelayed(
            {
                errorDialog!!.show()
                googleErrorView!!.findViewById<TextView>(R.id.text_error_message).text = message
                googleErrorView!!.findViewById<TextView>(R.id.button_retry).setOnClickListener {
                    errorDialog!!.hide()
                }
            }, WAIT_FOR_CALL_DURATION
        )
    }

    private fun onError(message: String) {
        Log.i(TAG, "Error layout Visible on $message")
        isOnError = true
        HANDLER.postDelayed(
            {
                rotate!!.cancel()
                AnimatorSet().apply {
                    this.play(hide)
                }.start()
                errorText!!.text = message
                errorLayout!!.visibility = View.VISIBLE
            }, WAIT_FOR_CALL_DURATION
        )
    }

    private fun navigateNewUser() {
        Log.i(TAG, "Navigating to user onboarding")
        val intent = Intent(this, NewUserActivity::class.java)
        val p1: UtilPair<View, String> = UtilPair.create(binding.appIcon as View, "logo")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@SplashActivity, p1)
        startActivity(intent, options.toBundle())
    }

    private fun navigateMain() {
        Log.i(TAG, "Navigating to home")
        val intent = Intent(this, MainActivity::class.java)
        val p1: UtilPair<View, String> = UtilPair.create(binding.appIcon as View, "logo")
        val p2: UtilPair<View, String> = UtilPair.create(binding.appName as View, "name")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@SplashActivity, p1, p2)
        startActivity(intent, options.toBundle())
    }
}