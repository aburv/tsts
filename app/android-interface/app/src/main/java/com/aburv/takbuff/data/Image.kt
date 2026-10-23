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
import android.util.LruCache
import androidx.core.graphics.createBitmap
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.net.HttpURLConnection
import java.net.URL

class Image(private val context: Context) : APIRequest(context) {

    companion object {
        private const val TAG = "App-IMAGE"
        private const val NAMESPACE: String = "image"
        private const val CACHE_SIZE_KB = 8 * 1024
        private val bitmapCache = object : LruCache<String, Bitmap>(CACHE_SIZE_KB) {
            override fun sizeOf(key: String, value: Bitmap): Int {
                return value.byteCount / 1024
            }
        }
    }

    @OptIn(DelicateCoroutinesApi::class)
    fun load(id: String, size: String, data: SetImage) {
        val path = "$DOMAIN/$NAMESPACE/$id/$size"
        Log.i(TAG, "Get $NAMESPACE/$id/$size")
        bitmapCache.get(path)?.let { bitmap ->
            Log.i(TAG, "Cache hit $path")
            GlobalScope.launch(Dispatchers.Main) {
                data.set(bitmap)
            }
            return
        }

        GlobalScope.launch(Dispatchers.IO) {
            val url = URL(path)
            val httpURLConnection = url.openConnection() as HttpURLConnection
            setHeaders(httpURLConnection)
            httpURLConnection.connect()
            val bitmap = BitmapFactory.decodeStream(httpURLConnection.inputStream)
            if (bitmap != null) {
                bitmapCache.put(path, bitmap)
            }
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