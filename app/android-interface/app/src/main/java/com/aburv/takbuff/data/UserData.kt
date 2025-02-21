package com.aburv.takbuff.data

import android.util.Log
import androidx.lifecycle.MutableLiveData
import org.json.JSONObject

class UserData {
    companion object {
        const val NAMESPACE: String = "user/"
    }

    var data = MutableLiveData<JSONObject>()

    fun getUserdata() {
        val path = "${NAMESPACE}app"
        try {
            APIRequest().get(path, object : Response {
                override fun onData(value: String) {
                    data.postValue(JSONObject(value))
                }

                override fun onError(value: String) {
                    data.postValue(JSONObject())
                }
            })
        } catch (e: Exception) {
            Log.e("Get user data", "Unable to retrieve")
        }
    }
}