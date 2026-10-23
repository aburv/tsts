package com.aburv.takbuff.playerDetailFragments

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import com.aburv.takbuff.adapters.ChipSet
import com.aburv.takbuff.adapters.ChipSetListAdapter
import com.aburv.takbuff.adapters.OptionData
import com.aburv.takbuff.data.PlayerFormData
import com.aburv.takbuff.databinding.FragmentPlayerStep3Binding
import org.json.JSONArray
import org.json.JSONObject


class Step3Fragment(
    private val context: Context,
    private var formData: PlayerFormData? = null
) : Fragment(),
    ChipSetListAdapter.OnChipClickEvent {

    private var selectedJerseySize: String? = null
    private var selectedShoeSize: String? = null
    private val selectedPositions = mutableSetOf<String>()
    private var onFormChanged: (() -> Unit)? = null

    private var selectedViewOnJ: ChipSetListAdapter.ViewHolder? = null
    private var selectedViewOnS: ChipSetListAdapter.ViewHolder? = null
    private val selectedViewsOnP: ArrayList<ChipSetListAdapter.ViewHolder> = arrayListOf()

    private var jerseySizeAdapter: ChipSetListAdapter? = null
    private var positionAdapter: ChipSetListAdapter? = null
    private var shoeSizeAdapter: ChipSetListAdapter? = null

    private var jerseySizes: ArrayList<OptionData> = arrayListOf()
    private var shoeSizes: ArrayList<OptionData> = arrayListOf()
    private var positions: ArrayList<OptionData> = arrayListOf(
    )
    private lateinit var binding: FragmentPlayerStep3Binding

    fun setFormData(value: PlayerFormData) {
        jerseySizes = value.jerseySizes
        shoeSizes = value.shoeSizes
        positions = value.positions
        jerseySizeAdapter?.setData(jerseySizes)
        shoeSizeAdapter?.setData(shoeSizes)
        positionAdapter?.setData(positions)
    }

    fun setOnFormChanged(listener: () -> Unit) {
        onFormChanged = listener
    }

    fun isValid(): Boolean {
        return selectedJerseySize != null && selectedShoeSize != null && selectedPositions.isNotEmpty()
       && binding.jerseyLayout.getJerseyName().isNotEmpty() &&
            binding.jerseyLayout.getJerseyNumber().isNotEmpty()

    }

    fun collectData(): JSONObject = JSONObject().apply {
        put("jName", binding.jerseyLayout.getJerseyName())
        put("jNo", binding.jerseyLayout.getJerseyNumber())
        put("jSize", selectedJerseySize)
        put("sSize", selectedShoeSize)
        put("positions", JSONArray(selectedPositions.toList()))
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentPlayerStep3Binding.inflate(inflater, container, false)
        val jersey = binding.jerseyLayout

        jersey.getJerseyName()

        jerseySizeAdapter =
            ChipSetListAdapter(context.theme!!, ChipSet.JERSEY_SIZE, jerseySizes, this)
        binding.listJerseySize.adapter = jerseySizeAdapter
        binding.listJerseySize.layoutManager =
            GridLayoutManager(context, 4, GridLayoutManager.VERTICAL, false)

        shoeSizeAdapter =
            ChipSetListAdapter(context.theme!!, ChipSet.SHOE_SIZE, shoeSizes, this)
        binding.listShoeSize.adapter = shoeSizeAdapter
        binding.listShoeSize.layoutManager =
            GridLayoutManager(context, 5, GridLayoutManager.VERTICAL, false)

        positionAdapter =
            ChipSetListAdapter(context.theme!!, ChipSet.POSITION, positions, this)
        binding.listPosition.adapter = positionAdapter
        binding.listPosition.layoutManager =
            GridLayoutManager(context, 3, GridLayoutManager.VERTICAL, false)
        formData?.let { setFormData(it) }

        onFormChanged?.invoke()
        return binding.root
    }

    override fun onChipSelect(type: ChipSet, view: ChipSetListAdapter.ViewHolder, id: String) {
        when (type) {
            ChipSet.SHOE_SIZE -> {
                if (selectedViewOnS == view) {
                    selectedViewOnS = null
                    selectedShoeSize = null
                } else {
                    selectedViewOnS?.setOther()
                    selectedViewOnS = view
                    selectedShoeSize = id
                }
            }

            ChipSet.JERSEY_SIZE -> {
                if (selectedViewOnJ == view) {
                    selectedViewOnJ = null
                    selectedJerseySize = null
                } else {
                    selectedViewOnJ?.setOther()
                    selectedViewOnJ = view
                    selectedJerseySize = id
                }
            }

            ChipSet.POSITION -> {
                if (view in selectedViewsOnP) {
                    selectedViewsOnP.remove(view)
                    selectedPositions.remove(id)
                } else {
                    selectedViewsOnP.add(view)
                    selectedPositions.add(id)
                }
            }

            else -> {}
        }
        view.toggleAndRenderUI()
        onFormChanged?.invoke()
    }
}
