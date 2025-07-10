package com.aburv.takbuff.data

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.PorterDuff
import android.graphics.PorterDuffXfermode
import android.graphics.Rect
import android.graphics.RectF
import android.util.Log
import androidx.core.graphics.createBitmap
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.net.HttpURLConnection
import java.net.URL

class Image(private val context: Context) : APIRequest(context) {

    companion object {
        private const val TAG = "App-Device"
        private const val NAMESPACE: String = "image/"
    }

    @OptIn(DelicateCoroutinesApi::class)
    fun load(id: String, size: String, data: SetImage) {
        val path = "$DOMAIN/$NAMESPACE/$id/$size"
        Log.i(TAG, "Get $path")
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

object ImageViewUtil {
    fun getRoundedCornerBitmap(bitmap: Bitmap, cornerRadius: Float): Bitmap {
        val output = createBitmap(bitmap.width, bitmap.height)
        val canvas = Canvas(output)

        val paint = Paint(Paint.ANTI_ALIAS_FLAG)
        val rect = Rect(0, 0, bitmap.width, bitmap.height)
        val rectF = RectF(rect)

        canvas.drawRoundRect(rectF, cornerRadius, cornerRadius, paint)

        // Draw the bitmap over the rounded shape
        paint.xfermode = PorterDuffXfermode(PorterDuff.Mode.SRC_IN)
        canvas.drawBitmap(bitmap, rect, rect, paint)

        return output
    }
}

fun interface SetImage {
    fun set(value: Bitmap)
}