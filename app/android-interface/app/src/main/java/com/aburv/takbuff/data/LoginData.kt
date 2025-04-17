package com.aburv.takbuff.data

import android.content.Context
import android.util.Log
import com.aburv.takbuff.db.AppUser
import com.aburv.takbuff.db.AppUserToken
import com.aburv.takbuff.db.DeviceDB
import com.aburv.takbuff.db.UserDB
import com.aburv.takbuff.db.UserTokenDB
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject

class Auth(private val context: Context) {
    companion object {
        private const val TAG = "App-LoginData"
        private const val NAMESPACE: String = "auth/"
    }

    suspend fun login(
        name: String,
        picUrl: String,
        email: String,
        googleId: String,
        location: Pair<String, String>?,
        response: LoginResponse
    ) {
        Log.i(TAG, "Login Call")
        val deviceDb = DeviceDB(context)
        val userTokenDb = UserTokenDB(context)
        val userDb = UserDB(context)
        val path = "${NAMESPACE}login"

        val locationData = JSONObject()
        if (location != null) {
            locationData.put("lat", location.first)
            locationData.put("long", location.second)
        }
        var deviceId = ""
        val devices = deviceDb.getDevices()
        if (devices.isNotEmpty()) {
            deviceId = devices[0].appDeviceId
            Log.i("Device done", deviceId)
        }
        Log.i("Device", deviceId)
        val loginData = JSONObject()

        loginData.put("deviceId", deviceId)
        loginData.put("location", locationData)

        val uIdData = JSONObject()
        uIdData.put("gId", googleId)
        uIdData.put("value", email)
        uIdData.put("type", "M")

        val userData = JSONObject()
        userData.put("name", name)
        userData.put("picurl", picUrl)
        userData.put("uId", uIdData)

        val data = JSONObject()

        data.put("user", userData)
        data.put("login", loginData)
        Log.i("Data", data.toString())

        try {
            APIRequest(context).post(path, data, object : Response {
                override fun onData(value: String) {
                    Log.i(TAG, "Received Tokens")

                    val resData = JSONObject(value)

                    val idToken = resData.getString("idToken")
                    val accessToken = resData.getString("accessToken")

                    val appUserToken = AppUserToken(
                        isActive = true,
                        accessToken = accessToken,
                        idToken = idToken,
                    )
                    val idPayload: JSONObject? = AuthUtil.parseToken(idToken)

                    if (idPayload != null) {
                        val userId = AuthUtil.getData(idPayload, "user.id") ?: ""
                        val userDp = AuthUtil.getData(idPayload, "user.dp") ?: ""
                        val userName = AuthUtil.getData(idPayload, "user.name") ?: ""
                        val userEmail = AuthUtil.getData(idPayload, "user.user_id.val") ?: ""

                        val appUser = AppUser(
                            isActive = true,
                            id = userId,
                            email = userEmail,
                            dp = userDp,
                            name = userName
                        )

                        CoroutineScope(Dispatchers.Default).launch {
                            userTokenDb.insertUserToken(appUserToken)
                            userDb.insertUser(appUser)
                        }

                        val accessPayload: JSONObject? = AuthUtil.parseToken(accessToken)
                        val isNew = isNewToApp(accessPayload!!)
                        if (isNew)
                            response.onNewUser()
                        else
                            response.onExistingUser()
                    }
                }

                override fun onError(value: String) {
                    Log.e("Login Call", value)
                    response.onError(value)
                }
            })
        } catch (e: Exception) {
            Log.i(TAG, "Failed in get auth info: $e")
        }
    }

    private fun isNewToApp(accessPayload: JSONObject): Boolean {
        val accesses: JSONArray = accessPayload.getJSONArray("accesses")
        for (i in 0 until accesses.length()) {
            val accessValue = accesses.get(i) as JSONObject

            for (key in accessValue.keys()) {
                if (key == "object_type") {
                    val value = accessValue.getString(key)
                    if (value == "U") {
                        return false
                    }
                }
            }
        }
        return true
    }

    suspend fun refreshToken() {
        Log.i(TAG, "Login Call")
        val path = "${NAMESPACE}refresh_token"
        try {
            APIRequest(context).get(path, object : Response {
                override fun onData(value: String) {
                    val resData = JSONObject(value)

                    val idToken = resData.getString("idToken")
                    val accessToken = resData.getString("accessToken")
                    val userTokenDb = UserTokenDB(context)
                    val appUserToken = AppUserToken(
                        isActive = true,
                        accessToken = accessToken,
                        idToken = idToken,
                    )
                    CoroutineScope(Dispatchers.Default).launch {
                        userTokenDb.updateUserToken(appUserToken)
                    }
                }

                override fun onError(value: String) {
                }
            })
        } catch (e: Exception) {
            Log.i(TAG, "Refresh $e.stackTraceToString()")
        }
    }
}

interface LoginResponse {
    fun onNewUser()
    fun onExistingUser()
    fun onError(message: String)
}

object AuthUtil {
    fun parseToken(idToken: String): JSONObject? {
        val parts = idToken.split(".")
        if (parts.size != 3) return null

        try {
            val payload = String(android.util.Base64.decode(parts[1], android.util.Base64.URL_SAFE))
            Log.i("Parse", payload)
            return JSONObject(payload)
        } catch (e: Exception) {
            Log.i("Parse token", e.toString())
            return null
        }
    }

    fun getData(data: JSONObject, key: String): String? {
        val keys = key.split(".")
        var current: JSONObject = data

        for ((index, currentKey) in keys.withIndex()) {
            if (index == keys.lastIndex) {
                return current.optString(currentKey)
            }
            current = current.optJSONObject(currentKey) ?: return null
        }
        return null
    }
}