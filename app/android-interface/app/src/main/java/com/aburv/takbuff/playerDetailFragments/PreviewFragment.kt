package com.aburv.takbuff.playerDetailFragments

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.graphics.Canvas
import android.graphics.Bitmap
import android.graphics.Bitmap.createBitmap
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.FileProvider
import androidx.fragment.app.Fragment
import com.aburv.takbuff.BuildConfig
import com.aburv.takbuff.R
import com.aburv.takbuff.databinding.FragmentPlayerPreviewBinding
import org.json.JSONObject
import java.io.File


class PreviewFragment(
    private val context: Context,
    private val jerseyData: JSONObject? = null
) : Fragment() {

    companion object {
        private const val TAG = "App-Fragment-Preview"
    }

    private lateinit var binding: FragmentPlayerPreviewBinding

    private val shareTargets = mapOf(
        R.id.button_whatsapp to ("com.whatsapp" to "Your game. Your jersey. Your story. #Takbuff"),
        R.id.button_facebook to ("com.facebook.katana" to "Meet the player behind the jersey. #Takbuff"),
        R.id.button_instagram to ("com.instagram.android" to "Built for the game. Worn with pride. #Takbuff"),
        R.id.button_snapshot to ("com.snapchat.android" to "New jersey, same love for the game. #Takbuff")
    )

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentPlayerPreviewBinding.inflate(inflater, container, false)
        binding.jerseyName.text = jerseyData?.optString("jName").orEmpty()
        binding.jerseyNumber.text = jerseyData?.optString("jNo").orEmpty()
        shareTargets.forEach { (viewId, target) ->
            binding.root.findViewById<View>(viewId).setOnClickListener {
                sharePoster(target.first, target.second)
            }
        }

        return binding.root
    }

    private fun sharePoster(packageName: String, caption: String) {
        val poster = renderPoster() ?: return
        val sharedDirectory = File(requireContext().cacheDir, "shared")
        sharedDirectory.mkdirs()
        val imageFile = File(sharedDirectory, "takbuff-player.jpg")
        imageFile.outputStream().use { output ->
            poster.compress(Bitmap.CompressFormat.JPEG, 95, output)
        }
        val uri = FileProvider.getUriForFile(
            requireContext(),
            "${BuildConfig.APPLICATION_ID}.fileprovider",
            imageFile
        )
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "image/jpeg"
            putExtra(Intent.EXTRA_STREAM, uri)
            putExtra(Intent.EXTRA_TEXT, caption)
            setPackage(packageName)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        try {
            startActivity(intent)
        } catch (_: ActivityNotFoundException) {
            Toast.makeText(context, R.string.social_app_not_installed, Toast.LENGTH_SHORT).show()
        }
    }

    private fun renderPoster(): Bitmap? {
        if (binding.layoutPoster.width <= 0 || binding.layoutPoster.height <= 0) return null
        val bitmap = createBitmap(
            binding.layoutPoster.width,
            binding.layoutPoster.height,
            Bitmap.Config.ARGB_8888
        )
        binding.layoutPoster.draw(Canvas(bitmap))
        return bitmap
    }
}