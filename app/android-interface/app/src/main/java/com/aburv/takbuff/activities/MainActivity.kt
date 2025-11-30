package com.aburv.takbuff.activities

import android.animation.Animator
import android.content.Intent
import android.content.pm.ActivityInfo
import android.location.Location
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewAnimationUtils
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.view.inputmethod.InputMethodManager
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.app.ActivityOptionsCompat
import androidx.core.util.Pair as UtilPair
import com.aburv.takbuff.R
import com.aburv.takbuff.data.Auth
import com.aburv.takbuff.data.AuthUtil
import com.aburv.takbuff.data.Image
import com.aburv.takbuff.data.ImageViewUtil
import com.aburv.takbuff.data.LocationData
import com.aburv.takbuff.data.LoginResponse
import com.aburv.takbuff.data.UserData
import com.aburv.takbuff.databinding.ActivityMainBinding
import com.aburv.takbuff.db.AppUser
import com.aburv.takbuff.mainFragments.DashboardFragment
import com.aburv.takbuff.services.GAuthService
import com.aburv.takbuff.services.GoogleAuthResponse
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.google.android.material.bottomsheet.BottomSheetDialog
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Dispatchers.Main
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    companion object {
        private const val TAG = "App-Main"

        private const val WAIT_FOR_CALL_DURATION = 1000L

        private val HANDLER = Handler(Looper.getMainLooper())
    }

    private lateinit var binding: ActivityMainBinding

    private var user: AppUser? = null

    private var clearIcon: ImageView? = null
    private var loaderLayout: ConstraintLayout? = null
    private var loadingAppLogo: ImageView? = null
    private var profile: ImageView? = null

    private var googleErrorView: View? = null
    private var errorDialog: BottomSheetDialog? = null

    private var searchingValue: String = ""

    private var loadingRotate: Animation? = null

    private var userData: UserData? = null
    private var authData: Auth? = null
    private var locationData: LocationData? = null

    private var location: Location? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.i(TAG, "On Create")

        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()

        requestedOrientation = if (resources.getBoolean(R.bool.isTablet)) {
            ActivityInfo.SCREEN_ORIENTATION_SENSOR
        } else {
            ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        }

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        userData = UserData(this)
        authData = Auth(this)
        locationData = LocationData(this)

        val extras = intent.extras
        if (extras == null) {
            supportFragmentManager
                .beginTransaction()
                .add(R.id.container, DashboardFragment(this))
                .commit()
        }

        if (extras != null) {
            val type: String = extras.getString("type", "")
            val id: String = extras.getString("id", "")
            loadFragment(type, id)
        }

        clearIcon = binding.icClear
        loaderLayout = binding.loadingLayout
        loadingAppLogo = binding.loadingAppIcon

        val searchIcon = binding.icSearch
        val searchLayout = binding.layoutSearch
        val closeIcon = binding.icBack
        val searchText = binding.searchInputText
        val searchList = binding.listSearch

        profile = binding.icProfile

        errorDialog = BottomSheetDialog(this, R.style.AppBottomSheetDialogTheme)

        googleErrorView = LayoutInflater.from(this)
            .inflate(R.layout.layout_bottom_error_dialog, null)
        errorDialog!!.setContentView(googleErrorView!!)

        loadingRotate = AnimationUtils.loadAnimation(this, R.anim.rotate)
        loadingRotate!!.fillAfter = true
        setLoadingOff()

        updateSearchCloseIcon()
        CoroutineScope(Main).launch {
            user = userData!!.getUser()
            updateProfileLogo()
        }

        searchIcon.setOnClickListener {
            Log.i(TAG, "Search Button pressed")

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
            Log.i(TAG, "Close Button pressed")

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
            Log.i(TAG, "Clear Button pressed")

            searchText.text.clear()
        }

        searchText.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable) {
                searchingValue = s.toString()
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

        profile!!.setOnClickListener {
            Log.i(TAG, "Profile Button pressed $user")

            if (user != null) {
                navigateUser()
            } else {
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
        }

        onBackPressedDispatcher.addCallback(
            this,
            object : OnBackPressedCallback(true) {
                override fun handleOnBackPressed() {
                    Log.i(TAG, "On Back pressed")
                    finishAffinity()
                }
            })

        binding.appIcon.setOnClickListener {
            navigateToDashboard()
        }
    }

    private suspend fun appLogin(googleUser: GoogleIdTokenCredential) {
        Log.i(TAG, "Login api Start")
        val locationData: Pair<String, String>? = if (location != null)
            Pair(location!!.latitude.toString(), location!!.longitude.toString())
        else null
        authData!!.login(
            googleUser.displayName!!,
            googleUser.profilePictureUri.toString(),
            googleUser.id,
            AuthUtil.getData(AuthUtil.parseToken(googleUser.idToken)!!, "sub")!!,
            locationData,
            object : LoginResponse {
                override fun onNewUser() {
                    Log.i(TAG, "On new user")
                    navigateNewUser()
                }

                override fun onExistingUser() {
                    Log.i(TAG, "On existing user")
                    CoroutineScope(Main).launch {
                        user = userData!!.getUser()
                        updateProfileLogo()
                    }
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
            },
            WAIT_FOR_CALL_DURATION
        )
    }

    private fun loadFragment(type: String, id: String?) {
        Log.i(TAG, "Load fragment $type")

        val fragment = when (type) {
            else -> DashboardFragment(this)
        }

        supportFragmentManager
            .beginTransaction()
            .add(R.id.container, fragment)
            .commit()
    }

    private fun setLoadingOn() {
        Log.i(TAG, "Loading ON")

        loaderLayout!!.visibility = View.VISIBLE
        loadingAppLogo!!.startAnimation(loadingRotate!!)
    }

    private fun setLoadingOff() {
        Log.i(TAG, "Loading OFF")

        loaderLayout!!.visibility = View.GONE
        loadingRotate!!.cancel()
    }

    private fun updateSearchCloseIcon() {
        Log.i(TAG, "Update search close icon")

        if (searchingValue.isNotBlank()) {
            clearIcon!!.visibility = View.VISIBLE
        } else {
            clearIcon!!.visibility = View.INVISIBLE
        }
    }

    private fun updateProfileLogo() {
        val image = Image(this)
        if (user == null) {
            profile!!.setImageResource(R.drawable.ic_google)
        } else {
            if (user!!.dp == "") {
                profile!!.setImageResource(R.drawable.ic_person)
            } else {
                profile!!.setPadding(0, 0, 0, 0)
                image.load(user!!.dp, "80") { data ->
                    val roundedImageData = ImageViewUtil.getRoundedCornerBitmap(data, 30.0F)
                    profile!!.setImageBitmap(roundedImageData)
                }
            }
        }
    }

    private fun navigateUser() {
        Log.i(TAG, "Navigate to User")

        val intent = Intent(this, UserActivity::class.java)
        val p1: UtilPair<View, String> = UtilPair.create(binding.icProfile as View, "dp")
        val p2: UtilPair<View, String> = UtilPair.create(binding.appIcon as View, "logo")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@MainActivity, p1, p2)
        startActivity(intent, options.toBundle())
    }

    private fun navigateNewUser() {
        Log.i(TAG, "Navigate to New User")

        val intent = Intent(this, NewUserActivity::class.java)
        val p1: UtilPair<View, String> = UtilPair.create(binding.appIcon as View, "logo")
        val options = ActivityOptionsCompat.makeSceneTransitionAnimation(this@MainActivity, p1)
        startActivity(intent, options.toBundle())
    }

    private fun navigateToDashboard() {
        Log.i(TAG, "Navigate to Dashboard")

        supportFragmentManager
            .beginTransaction()
            .replace(R.id.container, DashboardFragment(this))
            .commit()
    }
}