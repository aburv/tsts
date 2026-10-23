package com.aburv.takbuff.playerDetailFragments

import android.animation.AnimatorSet
import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.content.res.Resources
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.animation.LinearInterpolator
import androidx.fragment.app.Fragment
import com.aburv.takbuff.R
import com.aburv.takbuff.databinding.FragmentPlayerStep1Binding


//import androidx.navigation.fragment.FragmentNavigatorExtras
//import androidx.navigation.fragment.findNavController

class Step1Fragment : Fragment() {

    private lateinit var binding: FragmentPlayerStep1Binding

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentPlayerStep1Binding.inflate(inflater, container, false)

//        val extras = FragmentNavigatorExtras(
//            image to "user_pic"
//        )
//        findNavController().navigate(R.id.user_image, null, null, extras)

        return binding.root
    }
}
