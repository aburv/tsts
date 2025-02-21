package com.aburv.takbuff.data

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.net.HttpURLConnection
import java.net.URL

class Image : APIRequest() {

    @OptIn(DelicateCoroutinesApi::class)
    fun load(id: String, data: SetImage) {
        val path = "$DOMAIN/image/$id"
        GlobalScope.launch(Dispatchers.IO) {
            val url = URL(path)
            val httpURLConnection = url.openConnection() as HttpURLConnection
            setHeaders(httpURLConnection)
            httpURLConnection.connect()
            val bitmap = BitmapFactory.decodeStream(httpURLConnection.inputStream)
            launch(Dispatchers.Main) {
                data.set(bitmap)
            }
        }
    }
}

fun interface SetImage {
    fun set(value: Bitmap)
}