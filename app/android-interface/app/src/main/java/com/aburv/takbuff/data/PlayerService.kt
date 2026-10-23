package com.aburv.takbuff.data

import android.content.Context
import android.util.Log
import com.aburv.takbuff.adapters.OptionData
import org.json.JSONArray
import org.json.JSONObject

data class PlayerFormData(
    val bloodGroups: ArrayList<OptionData>,
    val genders: ArrayList<OptionData>,
    val jerseySizes: ArrayList<OptionData>,
    val shoeSizes: ArrayList<OptionData>,
    val positions: ArrayList<OptionData>
)

class PlayerService(private val context: Context) {

    companion object {
        private const val TAG = "App-Player"
        private const val NAMESPACE: String = "player"
    }

    suspend fun getFormData(response: PlayerFormDataResponse) {
        Log.i(TAG, "Get Form Data")
        APIRequest(context).get("${NAMESPACE}/form_data", object : Response {
            override fun onData(value: String) {
                try {
                    val data = JSONObject(value)
                    response.onData(
                        PlayerFormData(
                            options(data, "bGroup"),
                            options(data, "gender"),
                            options(data, "jSize"),
                            options(data, "sSize"),
                            options(data, "position")
                        )
                    )
                } catch (e: Exception) {
                    response.onError("Unable to parse player form data: $e")
                }
            }

            override fun onError(value: String) {
                response.onError(value)
            }
        })
    }

    suspend fun getActualPlayer(response: PlayerActualDataResponse) {
        Log.i(TAG, "Get Actual Player")
        APIRequest(context).get("${NAMESPACE}/actual/1", object : Response {
            override fun onData(value: String) {
                try {
                    response.onData(value)
                } catch (e: Exception) {
                    response.onError("Unable to parse actual player data: $e $value")
                }
            }

            override fun onError(value: String) {
                response.onError(value)
            }
        })
    }

    suspend fun getActualPlayerGear(response: PlayerActualDataResponse) {
        Log.i(TAG, "Get Actual Player")
        APIRequest(context).get("${NAMESPACE}/actual/2", object : Response {
            override fun onData(value: String) {
                try {
                    response.onData(value)
                } catch (e: Exception) {
                    response.onError("Unable to parse actual player data: $e")
                }
            }

            override fun onError(value: String) {
                response.onError(value)
            }
        })
    }

    suspend fun create(data: JSONObject, response: Response) {
        Log.i(TAG, "Create API call")
        APIRequest(context).post("${NAMESPACE}/", data, response) { body ->
            body.toString().replace(
                Regex("\"(weight|height)\":(-?\\d+)([,}])"),
                "\"$1\":$2.0$3"
            )
        }
    }

    suspend fun updateJersey(data: JSONObject, response: Response) {
        Log.i(TAG, "Update Jersey API call")
        APIRequest(context).post("${NAMESPACE}/jersey_details", data, response)
    }

    private fun options(data: JSONObject, key: String): ArrayList<OptionData> {
        val values = data.optJSONArray(key) ?: return arrayListOf()
        return ArrayList(values.toOptionData())
    }

    private fun JSONArray.toOptionData(): List<OptionData> {
        return List(length()) { index ->
            val option = getJSONObject(index)
            OptionData(option.getString("id"), option.getString("value"))
        }
    }
}

interface PlayerFormDataResponse {
    fun onData(value: PlayerFormData)
    fun onError(value: String)
}

interface PlayerActualDataResponse {
    fun onData(value: String)
    fun onError(value: String)
}
