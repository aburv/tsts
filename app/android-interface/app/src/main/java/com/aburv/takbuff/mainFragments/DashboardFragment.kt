package com.aburv.takbuff.mainFragments

import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.aburv.takbuff.databinding.FragmentDashboardBinding

class DashboardFragment(private val context: Context) : Fragment() {

     companion object {
        private const val TAG = "App-Dashboard"
    }
    
    private lateinit var binding: FragmentDashboardBinding

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        Log.i(TAG, "On Create")
        binding = FragmentDashboardBinding.inflate(inflater, container, false)
        return binding.root
    }
}