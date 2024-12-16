package com.aburv.takbuff.data

import android.annotation.SuppressLint
import android.content.Context
import android.os.Build
import android.provider.Settings
import android.util.Log
import com.aburv.takbuff.R
import com.aburv.takbuff.db.AppUserDevice
import com.aburv.takbuff.db.DeviceDB
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject

class DeviceData {
    companion object {
        const val NAMESPACE: String = "device/"
    }

    fun isDeviceRegistered(context: Context) {
        val deviceDb = DeviceDB(context)

        CoroutineScope(Dispatchers.Default).launch {
            val devices: List<AppUserDevice> = deviceDb.getDevices()
            if (devices.isEmpty()) {
                sendDeviceData(context, deviceDb)
            }
        }
    }

    @SuppressLint("HardwareIds")
    private fun sendDeviceData(context: Context, deviceDB: DeviceDB) {
        val isTablet = context.resources.getBoolean(R.bool.isTablet)
        val deviceId =
            Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID)
        val path = "${NAMESPACE}register"
        val data = JSONObject()
        val otherDetails = arrayOf(
            Build.VERSION.SDK_INT.toString(),
            Build.VERSION.BASE_OS,
            Build.VERSION.RELEASE,
            Build.VERSION.CODENAME,
            Build.VERSION.RELEASE_OR_CODENAME,
            Build.DEVICE,
            Build.ID,
            Build.HOST,
            Build.BOARD,
            Build.BOOTLOADER,
            Build.BRAND,
            Build.MANUFACTURER,
            Build.MODEL,
            Build.PRODUCT, Build.USER
        )
        data.put("deviceId", deviceId)
        data.put("os", "Android")
        data.put("version", Build.VERSION.RELEASE)
        data.put("other", otherDetails.joinToString(separator = " "))
        data.put("deviceType", if (isTablet) "Tablet" else "Phone")
        data.put("platform", "App")

        try {
            APIRequest().post(path, data, object : Response {
                override fun onData(value: String) {
                    val newDevise = AppUserDevice(
                        appDeviceId = value,
                        isActive = true,
                        id = null,
                        email = null,
                        name = null,
                        dp = null,
                        accessKey = null
                    )
                    CoroutineScope(Dispatchers.Default).launch {
                        deviceDB.insertDevice(newDevise)
                    }
                }

                override fun onError(value: String) {}
            })
        } catch (e: Exception) {
            Log.e("API Call", "Failed in posting device info")
        }
    }
}