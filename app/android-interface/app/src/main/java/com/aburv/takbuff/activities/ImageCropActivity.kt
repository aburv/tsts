package com.aburv.takbuff.activities

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Matrix
import android.graphics.Paint
import android.graphics.PointF
import android.graphics.RectF
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import android.widget.FrameLayout
import android.widget.ImageView
import androidx.activity.OnBackPressedDispatcher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatImageView
import com.aburv.takbuff.databinding.ActivityImageCropBinding
import androidx.lifecycle.lifecycleScope
import com.aburv.takbuff.R
import com.aburv.takbuff.data.Response
import com.aburv.takbuff.data.UserData
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlin.math.hypot
import kotlin.math.min

class ImageCropActivity : AppCompatActivity() {

    private lateinit var binding: ActivityImageCropBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportActionBar?.hide()

        binding = ActivityImageCropBinding.inflate(layoutInflater)
        setContentView(binding.root)

        pickImage()

        binding.buttonCancel.setOnClickListener {
            pickImage()
        }

        binding.buttonBack.setOnClickListener {
            onBackPressedDispatcher.onBackPressed()
        }

        binding.buttonAccept.setOnClickListener {
            val cropped = binding.viewCrop.crop() ?: return@setOnClickListener
            binding.buttonCancel.visibility = View.GONE
            binding.buttonAccept.setImageResource(R.drawable.ic_loading_spinner)
            binding.buttonAccept.isEnabled = false
            binding.buttonAccept.startAnimation(
                android.view.animation.AnimationUtils.loadAnimation(
                    this,
                    R.anim.rotate
                )
            )
            upload(cropped)
        }
    }

    private val pickImageResult =
        registerForActivityResult(ActivityResultContracts.GetContent()) { uri ->
            if (uri == null) {
                onBackPressedDispatcher.onBackPressed()
                Log.i(TAG, "Image picker closed without selecting an image")
                return@registerForActivityResult
            }
            val bitmap = BitmapFactory.decodeStream(contentResolver.openInputStream(uri))
            binding.viewCrop.setImage(bitmap)
        }

    private fun pickImage() {
        pickImageResult.launch("image/*")
    }

    private fun upload(bitmap: Bitmap) {
        lifecycleScope.launch(Dispatchers.IO) {
            UserData(this@ImageCropActivity).uploadDisplayPicture(bitmap, object : Response {
                override fun onData(value: String) {
                    setResult(RESULT_OK, intent.putExtra(EXTRA_IMAGE_ID, value))
                    finish()
                }

                override fun onError(value: String) = showUploadError(value)
            })
        }
    }

    private fun showUploadError(message: String) {
        runOnUiThread {
            binding.buttonAccept.clearAnimation()
            binding.buttonAccept.setImageResource(R.drawable.ic_tick)
            binding.buttonCancel.visibility = View.VISIBLE
            binding.buttonAccept.isEnabled = true
            Toast.makeText(this, message, Toast.LENGTH_LONG).show()
        }
    }

    companion object {
        private const val TAG = "App-ImageCrop"
        const val EXTRA_IMAGE_ID = "image_id"
    }
}

class SmartCropView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : FrameLayout(context, attrs) {

    private val imageView = AppCompatImageView(context).apply {
        scaleType = ImageView.ScaleType.FIT_CENTER
    }

    private val cropMask = CropMaskView(context)
    private var imageBitmap: Bitmap? = null

    init {
        addView(imageView, LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
        addView(cropMask)
    }

    fun setImage(bitmap: Bitmap) {
        imageBitmap = bitmap
        post {
            imageView.layoutParams = LayoutParams(
                LayoutParams.MATCH_PARENT,
                LayoutParams.MATCH_PARENT
            )
            imageView.setImageBitmap(bitmap)

            imageView.post {
                val imageRect = imageView.getBitmapDisplayRect()
                val maskSize = min(imageRect.width(), imageRect.height()).toInt()
                cropMask.init(
                    maskSize,
                    maskSize,
                    imageRect.left,
                    imageRect.top,
                    imageRect.width(),
                    imageRect.height()
                )
            }
        }
    }

    fun ImageView.getBitmapDisplayRect(): RectF {
        val drawable = drawable ?: return RectF()
        val matrix = imageMatrix
        val bounds = drawable.bounds

        val values = FloatArray(9)
        matrix.getValues(values)

        val left = values[Matrix.MTRANS_X]
        val top = values[Matrix.MTRANS_Y]
        val width = bounds.width() * values[Matrix.MSCALE_X]
        val height = bounds.height() * values[Matrix.MSCALE_Y]

        return RectF(left, top, left + width, top + height)
    }

    fun crop(): Bitmap? {
        val bitmap = imageBitmap ?: return null

        val imageRect = imageView.getBitmapDisplayRect()
        val cropRect = cropMask.getCropRectFromView() // get raw rect in View space

        val intersected = RectF(
            (cropRect.left - imageRect.left).coerceAtLeast(0f),
            (cropRect.top - imageRect.top).coerceAtLeast(0f),
            (cropRect.right - imageRect.left).coerceAtMost(imageRect.width()),
            (cropRect.bottom - imageRect.top).coerceAtMost(imageRect.height())
        )

        val scaleX = bitmap.width / imageRect.width()
        val scaleY = bitmap.height / imageRect.height()

        val left = (intersected.left * scaleX).toInt()
        val top = (intersected.top * scaleY).toInt()
        val width = (intersected.width() * scaleX).toInt()
        val height = (intersected.height() * scaleY).toInt()

        return Bitmap.createBitmap(bitmap, left, top, width, height)
    }

}

class CropMaskView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null
) : View(context, attrs) {

    private val borderPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.WHITE
        style = Paint.Style.STROKE
        strokeWidth = 3f
    }
    private val gridPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.WHITE
        alpha = 100
        strokeWidth = 1f
    }
    private val handlePaint = Paint().apply {
        color = Color.WHITE
        style = Paint.Style.FILL
    }

    private val handleSize = 30f
    private var startX = 0f
    private var startY = 0f
    private var dragType = DragType.NONE
    private var cropRect = RectF()
    private var bounds = RectF()

    fun init(w: Int, h: Int, imgLeft: Float, imgTop: Float, imgW: Float, imgH: Float) {
        cropRect.set(
            imgLeft + (imgW - w) / 2f,
            imgTop + (imgH - h) / 2f,
            imgLeft + (imgW + w) / 2f,
            imgTop + (imgH + h) / 2f
        )
        bounds.set(imgLeft, imgTop, imgLeft + imgW, imgTop + imgH)
        invalidate()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        canvas.drawRect(cropRect, borderPaint)

        val thirdW = cropRect.width() / 3f
        val thirdH = cropRect.height() / 3f
        for (i in 1..2) {
            canvas.drawLine(
                cropRect.left + thirdW * i,
                cropRect.top,
                cropRect.left + thirdW * i,
                cropRect.bottom,
                gridPaint
            )
            canvas.drawLine(
                cropRect.left,
                cropRect.top + thirdH * i,
                cropRect.right,
                cropRect.top + thirdH * i,
                gridPaint
            )
        }

        drawHandle(canvas, cropRect.left, cropRect.top)
        drawHandle(canvas, cropRect.right, cropRect.top)
        drawHandle(canvas, cropRect.left, cropRect.bottom)
        drawHandle(canvas, cropRect.right, cropRect.bottom)
    }

    private fun drawHandle(canvas: Canvas, x: Float, y: Float) {
        canvas.drawCircle(x, y, handleSize / 2, handlePaint)
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        val x = event.x
        val y = event.y
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                dragType = detectDragType(x, y)
                startX = x
                startY = y
                return true
            }

            MotionEvent.ACTION_MOVE -> {
                val dx = x - startX
                val dy = y - startY
                when (dragType) {
                    DragType.MOVE -> moveRect(dx, dy)
                    DragType.RESIZE -> resizeRect(dx, dy)
                    DragType.NONE -> {}
                }
                startX = x
                startY = y
                invalidate()
                return true
            }

            MotionEvent.ACTION_UP -> dragType = DragType.NONE
        }
        return super.onTouchEvent(event)
    }

    private fun detectDragType(x: Float, y: Float): DragType {
        val corners = listOf(
            PointF(cropRect.left, cropRect.top),
            PointF(cropRect.right, cropRect.top),
            PointF(cropRect.left, cropRect.bottom),
            PointF(cropRect.right, cropRect.bottom)
        )
        return if (corners.any { hypot((it.x - x), (it.y - y)) < 80f }) DragType.RESIZE
        else if (cropRect.contains(x, y)) DragType.MOVE
        else DragType.NONE
    }

    private fun moveRect(dx: Float, dy: Float) {
        cropRect.offset(dx, dy)
        if (!bounds.contains(cropRect)) cropRect.offset(-dx, -dy)
    }

    private fun resizeRect(dx: Float, dy: Float) {
        val newSize = cropRect.width() + dx
        val maxSize = min(bounds.right - cropRect.left, bounds.bottom - cropRect.top)
        val finalSize = newSize.coerceIn(300f, maxSize)
        cropRect.right = cropRect.left + finalSize
        cropRect.bottom = cropRect.top + finalSize
    }

    fun getCropRectFromView(): RectF = RectF(cropRect)

    enum class DragType { NONE, MOVE, RESIZE }
}
