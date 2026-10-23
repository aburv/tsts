package com.aburv.takbuff.playerDetailFragments

//import androidx.navigation.fragment.findNavController
import android.animation.ObjectAnimator
import android.app.DatePickerDialog
import android.content.Context
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.util.TypedValue
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.annotation.ColorInt
import androidx.appcompat.content.res.AppCompatResources
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import com.aburv.takbuff.R
import com.aburv.takbuff.adapters.ChipSet
import com.aburv.takbuff.adapters.ChipSetListAdapter
import com.aburv.takbuff.adapters.OptionData
import com.aburv.takbuff.data.PlayerFormData
import com.aburv.takbuff.databinding.FragmentPlayerStep2Binding
import java.util.Calendar
import org.json.JSONObject
import androidx.core.view.isGone


class Step2Fragment(
    private val context: Context,
    private var formData: PlayerFormData? = null,
) : Fragment(),
    ChipSetListAdapter.OnChipClickEvent {

    private var selectedBloodGroup: String? = null
    private var selectedGender: String? = null
    private var selectedBirthDate: String? = null
    private var onFormChanged: (() -> Unit)? = null

    private var selectedViewOnBG: ChipSetListAdapter.ViewHolder? = null
    private var selectedViewOnG: ChipSetListAdapter.ViewHolder? = null

    private var bloodGroupAdapter: ChipSetListAdapter? = null
    private var genderAdapter: ChipSetListAdapter? = null
    private var bloodGroups: ArrayList<OptionData> = arrayListOf()
    private var genders: ArrayList<OptionData> = arrayListOf()
    private lateinit var binding: FragmentPlayerStep2Binding

    fun setFormData(value: PlayerFormData) {
        formData = value
        bloodGroups = value.bloodGroups
        genders = value.genders
        bloodGroupAdapter?.setData(bloodGroups)
        genderAdapter?.setData(genders)
    }

    fun setOnFormChanged(listener: () -> Unit) {
        onFormChanged = listener
    }

    fun isValid(): Boolean {
        return binding.editName.text.toString().trim().isNotEmpty() &&
                binding.editWeight.text.toString().toDoubleOrNull()?.let { it > 0 } == true &&
                binding.editHeight.text.toString().toDoubleOrNull()?.let { it > 0 } == true &&
                selectedBirthDate != null && selectedBloodGroup != null && selectedGender != null
    }

    fun collectData(): JSONObject = JSONObject().apply {
        put("callName", binding.editName.text.toString().trim())
        put("bloodGroup", selectedBloodGroup)
        put("gender", selectedGender)
        put("birthDate", selectedBirthDate)
        put("weight", binding.editWeight.text.toString().toBigDecimal().let {
            it.setScale(maxOf(1, it.scale()))
        })
        put("height", binding.editHeight.text.toString().toBigDecimal().let {
            it.setScale(maxOf(1, it.scale()))
        })
    }

    private val darkTypeValue = TypedValue()
    private val lessBrightTypeValue = TypedValue()
    private val theme = context.theme!!

    @ColorInt
    var dark: Int? = null

    @ColorInt
    var lessBright: Int? = null

    init {
        theme.resolveAttribute(R.attr.dark, darkTypeValue, true)
        theme.resolveAttribute(R.attr.lessBright, lessBrightTypeValue, true)
        dark = darkTypeValue.data
        lessBright = lessBrightTypeValue.data
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentPlayerStep2Binding.inflate(inflater, container, false)

        val editName = binding.editName
        val labelName = binding.labelName
        val editWeight = binding.editWeight
        val labelWeight = binding.labelWeight
        val editHeight = binding.editHeight
        val labelHeight = binding.labelHeight
        val textDob = binding.textDob
        val labelDob = binding.labelDob

        labelName.visibility = View.GONE
        editName.hint = getString(R.string.name)

        editName.setOnFocusChangeListener { _, hasFocus: Boolean ->
            if (hasFocus) {
                labelName.visibility = View.VISIBLE
                ObjectAnimator.ofFloat(
                    labelName,
                    "translationY",
                    0f,
                    -10f
                ) // Adjust the distance as needed
                    .setDuration(300)
                    .start()
                editName.hint = getString(R.string.text_name_hint)
                editName.background =
                    AppCompatResources.getDrawable(context, R.drawable.bg_input_focused)
            } else {
                if (editName.text.toString().isEmpty()) {
                    ObjectAnimator.ofFloat(labelName, "translationY", -10f, 0f)
                        .setDuration(300)
                        .start()
                    labelName.visibility = View.GONE
                    editName.hint = getString(R.string.name)
                }
                editName.background = AppCompatResources.getDrawable(context, R.drawable.bg_input)
            }
        }

        // Optionally, handle the case when the user starts typing even before focus
        editName.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(
                charSequence: CharSequence?,
                start: Int,
                count: Int,
                after: Int
            ) {
            }

            override fun onTextChanged(
                charSequence: CharSequence?,
                start: Int,
                before: Int,
                count: Int
            ) {
                if (charSequence?.isNotEmpty() == true && labelName.isGone) {
                    labelName.visibility = View.VISIBLE
                    ObjectAnimator.ofFloat(labelName, "translationY", 0f, -10f)
                        .setDuration(300)
                        .start()
                    editName.background =
                        AppCompatResources.getDrawable(context, R.drawable.bg_input_focused)
                }
            }

            override fun afterTextChanged(editable: Editable?) {}
        })
        editName.addTextChangedListener(formWatcher)

        // Initially, hide the label (it will only appear when focused)
        labelWeight.visibility = View.GONE
        editWeight.hint = getString(R.string.weight)

        editWeight.setOnFocusChangeListener { _, hasFocus ->
            if (hasFocus) {
                // Move the label up when EditText gains focus
                labelWeight.visibility = View.VISIBLE
                ObjectAnimator.ofFloat(
                    labelWeight,
                    "translationY",
                    0f,
                    -10f
                ) // Adjust the distance as needed
                    .setDuration(300)
                    .start()
                editWeight.hint = getString(R.string.text_weight_hint)
                editWeight.background =
                    AppCompatResources.getDrawable(context, R.drawable.bg_input_focused)
            } else {
                // Move the label down when EditText loses focus
                if (editWeight.text.toString().isEmpty()) {
                    ObjectAnimator.ofFloat(labelWeight, "translationY", -10f, 0f)
                        .setDuration(300)
                        .start()
                    labelWeight.visibility = View.GONE
                    editWeight.hint = getString(R.string.weight)
                }
                editWeight.background = AppCompatResources.getDrawable(context, R.drawable.bg_input)
            }
        }

        // Optionally, handle the case when the user starts typing even before focus
        editWeight.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(
                charSequence: CharSequence?,
                start: Int,
                count: Int,
                after: Int
            ) {
            }

            override fun onTextChanged(
                charSequence: CharSequence?,
                start: Int,
                before: Int,
                count: Int
            ) {
                if (charSequence?.isNotEmpty() == true && labelWeight.visibility == View.GONE) {
                    labelWeight.visibility = View.VISIBLE
                    ObjectAnimator.ofFloat(labelWeight, "translationY", 0f, -10f)
                        .setDuration(300)
                        .start()
                    editWeight.background =
                        AppCompatResources.getDrawable(context, R.drawable.bg_input_focused)
                }
            }

            override fun afterTextChanged(editable: Editable?) {}
        })
        editWeight.addTextChangedListener(formWatcher)

        // Initially, hide the label (it will only appear when focused)
        labelHeight.visibility = View.GONE
        editHeight.hint = getString(R.string.height)

        editHeight.setOnFocusChangeListener { _, hasFocus: Boolean ->
            if (hasFocus) {
                // Move the label up when EditText gains focus
                labelHeight.visibility = View.VISIBLE
                ObjectAnimator.ofFloat(
                    labelHeight,
                    "translationY",
                    0f,
                    -10f
                ) // Adjust the distance as needed
                    .setDuration(300)
                    .start()
                editHeight.hint = getString(R.string.text_height_hint)
                editHeight.background =
                    AppCompatResources.getDrawable(context, R.drawable.bg_input_focused)
            } else {
                // Move the label down when EditText loses focus
                if (editHeight.text.toString().isEmpty()) {
                    ObjectAnimator.ofFloat(labelHeight, "translationY", -10f, 0f)
                        .setDuration(300)
                        .start()
                    labelHeight.visibility = View.GONE
                    editHeight.hint = getString(R.string.height)
                }
                editHeight.background = AppCompatResources.getDrawable(context, R.drawable.bg_input)
            }
        }

        // Optionally, handle the case when the user starts typing even before focus
        editHeight.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(
                charSequence: CharSequence?,
                start: Int,
                count: Int,
                after: Int
            ) {
            }

            override fun onTextChanged(
                charSequence: CharSequence?,
                start: Int,
                before: Int,
                count: Int
            ) {
                if (charSequence?.isNotEmpty() == true && labelHeight.visibility == View.GONE) {
                    labelHeight.visibility = View.VISIBLE
                    ObjectAnimator.ofFloat(labelHeight, "translationY", 0f, -10f)
                        .setDuration(300)
                        .start()
                    editHeight.background =
                        AppCompatResources.getDrawable(context, R.drawable.bg_input)
                }
            }

            override fun afterTextChanged(editable: Editable?) {}
        })
        editHeight.addTextChangedListener(formWatcher)

        labelDob.visibility = View.GONE
        textDob.text = getString(R.string.dob)
        textDob.setTextColor(lessBright!!)

        binding.inputDob.setOnClickListener {
            val hasSelectedDate = textDob.text.toString() != getString(R.string.dob) &&
                    textDob.text.toString() != getString(R.string.text_date_placeholder)

            labelDob.visibility = View.VISIBLE
            if (textDob.text.toString() == getString(R.string.dob)) {
                textDob.text = getString(R.string.text_date_placeholder)
            }
            textDob.setTextColor(dark!!)
            textDob.background =
                AppCompatResources.getDrawable(context, R.drawable.bg_input_focused)

            // on below line we are getting
            // the instance of our calendar.
            val c = Calendar.getInstance()

            // on below line we are getting
            // our day, month and year.
            val year = c.get(Calendar.YEAR)
            val month = c.get(Calendar.MONTH)
            val day = c.get(Calendar.DAY_OF_MONTH)

            // on below line we are creating a
            // variable for date picker dialog.
            val datePickerDialog = DatePickerDialog(
                // on below line we are passing context.
                context, { _, selectedYear, monthOfYear, dayOfMonth ->
                    // on below line we are setting
                    // date to our text view.
                    binding.textDob.text =
                        ("$dayOfMonth/${monthOfYear + 1}/$selectedYear")
                    selectedBirthDate = String.format(
                        "%04d-%02d-%02d", selectedYear, monthOfYear + 1, dayOfMonth
                    )

                    binding.textDob.setTextColor(dark!!)
                    binding.textDob.background =
                        AppCompatResources.getDrawable(context, R.drawable.bg_input)
                },
                // on below line we are passing year, month
                // and day for the selected date in our date picker.
                year,
                month,
                day
            )
            datePickerDialog.setOnCancelListener {
                if (!hasSelectedDate) {
                    labelDob.visibility = View.GONE
                    textDob.text = getString(R.string.dob)
                    textDob.setTextColor(lessBright!!)
                }
                textDob.background =
                    AppCompatResources.getDrawable(context, R.drawable.bg_input)
                onFormChanged?.invoke()
            }
            // at last we are calling show
            // to display our date picker dialog.
            datePickerDialog.show()
        }

        bloodGroupAdapter =
            ChipSetListAdapter(context.theme!!, ChipSet.BLOOD_GROUP, bloodGroups, this)
        binding.listBloodGroup.adapter = bloodGroupAdapter
        binding.listBloodGroup.layoutManager =
            GridLayoutManager(context, 6, GridLayoutManager.VERTICAL, false)

        genderAdapter =
            ChipSetListAdapter(context.theme!!, ChipSet.GENDER, genders, this)
        binding.listGender.adapter = genderAdapter
        binding.listGender.layoutManager =
            GridLayoutManager(context, 2, GridLayoutManager.VERTICAL, false)
        formData?.let { setFormData(it) }

        onFormChanged?.invoke()
        return binding.root
    }

    override fun onChipSelect(type: ChipSet, view: ChipSetListAdapter.ViewHolder, id: String) {
        when (type) {
            ChipSet.BLOOD_GROUP -> {
                if (selectedViewOnBG == view) {
                    selectedViewOnBG = null
                    selectedBloodGroup = null
                } else {
                    selectedViewOnBG?.setOther()
                    selectedViewOnBG = view
                    selectedBloodGroup = id
                }
            }

            ChipSet.GENDER -> {
                if (selectedViewOnG == view) {
                    selectedViewOnG = null
                    selectedGender = null
                } else {
                    selectedViewOnG?.setOther()
                    selectedViewOnG = view
                    selectedGender = id
                }
            }

            else -> {}
        }
        view.toggleAndRenderUI()
        onFormChanged?.invoke()
    }

    private val formWatcher = object : TextWatcher {
        override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
        override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
            onFormChanged?.invoke()
        }

        override fun afterTextChanged(s: Editable?) = Unit
    }

}