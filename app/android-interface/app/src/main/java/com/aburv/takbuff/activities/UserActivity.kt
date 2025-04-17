package com.aburv.takbuff.activities

import android.content.Intent
import android.content.pm.PackageInfo
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.app.ActivityOptionsCompat
import androidx.core.util.Pair
import com.aburv.takbuff.R
import com.aburv.takbuff.data.Image
import com.aburv.takbuff.data.ImageViewUtil
import com.aburv.takbuff.data.UserData
import com.aburv.takbuff.databinding.ActivityUserBinding
import com.aburv.takbuff.db.AppUser
import com.aburv.takbuff.db.UserDB
import com.aburv.takbuff.db.UserTokenDB
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers.Main
import kotlinx.coroutines.launch
import java.time.LocalDate


class UserActivity : AppCompatActivity() {
    companion object {
        private const val TAG = "App-User"
    }

    private lateinit var binding: ActivityUserBinding
    private var user: AppUser? = null

    private var logo: ImageView? = null
    private var dp: ImageView? = null
    private var email: TextView? = null
    private var name: TextView? = null

    private var viewPlayer: ConstraintLayout? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        Log.i(TAG, "On Create")
        super.onCreate(savedInstanceState)
        supportActionBar!!.hide()

        binding = ActivityUserBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val signOut = binding.buttonSignout
        val back = binding.back
        val versionText = binding.textVersion
        val appName = binding.textProduct

        name = binding.userName
        email = binding.userEmail
        dp = binding.userDp
        logo = binding.appIcon
        viewPlayer = binding.buttonViewProfile

        val pInfo: PackageInfo = packageManager.getPackageInfo(packageName, 0)
        val version = pInfo.versionName
        val buildNUmber = pInfo.longVersionCode

        versionText.text = "Version $version.$buildNUmber"
        appName.text = "${getText(R.string.app_name)} © ${getThisYear()}"

        val userData = UserData(this)
        CoroutineScope(Main).launch {
            user = userData.getUser()
            setUserLayout()
        }
        back.setOnClickListener {
            Log.i(TAG, "Back button pressed")
            navigateMain()
        }

        signOut.setOnClickListener {
            Log.i(TAG, "Back button pressed")
            signOut()
        }

    }

    private fun getThisYear(): Int {
        return LocalDate.now().year
    }

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

    private fun signOut() {
        Log.i(TAG, "Sign out")

        val userDB = UserDB(this)
        val userTokenDB = UserTokenDB(this)

        CoroutineScope(Main).launch {
            userDB.deleteAll()
            userTokenDB.deleteAll()

            navigateMain()
        }
    }

    private fun navigateMain() {
        Log.i(TAG, "Navigate to main")
        val intent = Intent(this, MainActivity::class.java)
        val p1: Pair<View, String> = Pair.create(dp as View, "dp")
        val p2: Pair<View, String> = Pair.create(logo as View, "logo")
        val options =
            ActivityOptionsCompat.makeSceneTransitionAnimation(this@UserActivity, p1, p2)
        startActivity(intent, options.toBundle())
    }
}