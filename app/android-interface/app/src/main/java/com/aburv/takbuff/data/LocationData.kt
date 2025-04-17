package com.aburv.takbuff.data

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.util.Log
import androidx.core.app.ActivityCompat

class LocationData(private val context: Context) {

    private var locationManager: LocationManager? = null
    private var providers: ArrayList<String> = arrayListOf()
    
    init {
        try {
            Log.i(TAG, "Init Location")
            locationManager = context.getSystemService(Context.LOCATION_SERVICE) as LocationManager?
        } catch (e: Exception) {
            Log.i(TAG, "Error in Init Location $e")
        }
    }

    fun isAvailable() = providers.isNotEmpty()

    fun setProvider() {
        providers = arrayListOf()
        for (provider in locationManager!!.allProviders) {
            if (locationManager!!.isProviderEnabled(provider)) {
                providers.add(provider)
            }
        }
        Log.i(TAG, "Providers $providers")
    }

    fun getCurrentLocation(): Location? {
        Log.i(TAG, "Get current location by $providers")
        if (
            ActivityCompat.checkSelfPermission(context, FINE_LOCATION) != GRANTED &&
            ActivityCompat.checkSelfPermission(context, COARSE_LOCATION) != GRANTED
        ) {
            ActivityCompat.requestPermissions(
                context as Activity,
                arrayOf(FINE_LOCATION, COARSE_LOCATION),
                REQUEST_CODE
            )
        }

        for (provider in providers) {
            Log.i(TAG, "Get current location by $provider")
            val location = locationManager!!.getLastKnownLocation(provider)
            if (location != null) {
                return location
            }
        }
        Log.i(TAG, "No Location data from any provider")
        return null
    }

    fun requestPermission() {
        if (
            ActivityCompat.checkSelfPermission(context, FINE_LOCATION) != GRANTED &&
            ActivityCompat.checkSelfPermission(context, COARSE_LOCATION) != GRANTED
        ) {
            ActivityCompat.requestPermissions(
                context as Activity,
                arrayOf(FINE_LOCATION, COARSE_LOCATION),
                REQUEST_CODE
            )
        }
    }

    companion object {

        private const val TAG = "App-Location"
        private const val REQUEST_CODE = 101
        private const val GRANTED = PackageManager.PERMISSION_GRANTED
        private const val COARSE_LOCATION = Manifest.permission.ACCESS_COARSE_LOCATION
        private const val FINE_LOCATION = Manifest.permission.ACCESS_FINE_LOCATION

    }

}