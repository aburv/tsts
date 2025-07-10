package com.aburv.takbuff.data

import android.annotation.SuppressLint
import android.content.Context
import android.os.Build
import android.provider.Settings
import android.util.Log
import com.aburv.takbuff.R
import com.aburv.takbuff.db.AppDevice
import com.aburv.takbuff.db.DeviceDB
import com.aburv.takbuff.services.GAuthService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONObject

class DeviceData(private val context: Context) {
    companion object {
        private const val TAG = "App-Device"
        private const val NAMESPACE: String = "device/"
    }

    fun isDeviceRegistered() {
        val deviceDb = DeviceDB(context)

        CoroutineScope(Dispatchers.Default).launch {
            val devices: List<AppDevice> = deviceDb.getDevices()
            if (devices.isEmpty()) {
                Log.i(TAG, "No Device Registered")
                sendDeviceData(context, deviceDb)
            }
        }
    }

    @SuppressLint("HardwareIds")
    private suspend fun sendDeviceData(context: Context, deviceDB: DeviceDB) {
        Log.i(TAG, "Registering New device")

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
        data.put("deviceType", if (isTablet) "T" else "P")
        data.put("platform", "A")

        try {
            APIRequest(context).post(path, data, object : Response {
                override fun onData(value: String) {
                    val newDevise = AppDevice(
                        isActive = true,
                        appDeviceId = value
                    )
                    CoroutineScope(Dispatchers.Default).launch {
                        Log.i(TAG, "Device Registered")
                        deviceDB.insertDevice(newDevise)
                    }
                }

                override fun onError(value: String) {}
            })
        } catch (_: Exception) {
            Log.e("API Call", "Failed in posting device info")
        }
    }
}