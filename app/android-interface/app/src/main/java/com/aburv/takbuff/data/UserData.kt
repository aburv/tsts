package com.aburv.takbuff.data

import android.content.Context
import android.util.Log
import androidx.lifecycle.MutableLiveData
import com.aburv.takbuff.db.AppUser
import com.aburv.takbuff.db.UserDB
import org.json.JSONObject

class UserData(private val context: Context) {
    companion object {
        private const val TAG = "App-UserData"
        private const val NAMESPACE: String = "user/"
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
        val path = "${NAMESPACE}app"
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
            data.postValue(null)
            Log.e("Get user data", "Unable to retrieve $e")
        }
    }
}