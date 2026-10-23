package com.aburv.takbuff.data

import android.content.Context
import android.graphics.Bitmap
import android.util.Log
import androidx.lifecycle.MutableLiveData
import com.aburv.takbuff.db.AppUser
import com.aburv.takbuff.db.UserDB
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.ByteArrayOutputStream

class UserData(private val context: Context) {
    companion object {
        private const val TAG = "App-UserData"
        private const val NAMESPACE: String = "user"
    }

    var data = MutableLiveData<JSONObject>()
    var error = MutableLiveData<String>()

    suspend fun getUser(): AppUser? {
        val userDb = UserDB(context)
        val users: List<AppUser> = userDb.getUsers()
        if (users.isNotEmpty()) {
            Log.i(TAG, "No User data")
            return users[0]
        }
        return null
    }

    suspend fun getUserdata() {
        Log.i(TAG, "Get user data")
        val path = "${NAMESPACE}/app"
        try {
            APIRequest(context).get(path, object : Response {
                override fun onData(value: String) {
                    data.postValue(JSONObject(value))
                }

                override fun onError(value: String) {
                    data.postValue(JSONObject())
                }
            })
        } catch (e: Exception) {
            data.postValue(JSONObject())
            Log.e("Get user data", "Unable to retrieve $e")
        }
    }

    suspend fun setOnBoardingDone(response: Response) {
        Log.i(TAG, "Set done onboarding")
        val path = "${NAMESPACE}/done_onboarding"
        try {
            APIRequest(context).post(path, JSONObject(), object : Response {
                override fun onData(value: String) {
                    response.onData(value)
                }
                override fun onError(value: String) {
                    response.onError(value)
                }
            })
        } catch (e: Exception) {
            Log.e("Set user onboarding Done", "Unable to retrieve $e")
            response.onError(e.toString())
        }
    }

    suspend fun updateDisplayPicture(imageId: String) {
        val currentUser = getUser() ?: return
        UserDB(context).insertUser(currentUser.copy(dp = imageId))
    }

    suspend fun uploadDisplayPicture(bitmap: Bitmap, response: Response) {
        val output = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 90, output)
        APIRequest(context).upload("user/image", "profile.jpg", output.toByteArray(), object : Response {
            override fun onData(value: String) {
                CoroutineScope(Dispatchers.IO).launch {
                    updateDisplayPicture(value)
                    withContext(Dispatchers.Main) {
                        response.onData(value)
                    }
                }
            }

            override fun onError(value: String) {
                response.onError(value)
            }
        })
    }
}