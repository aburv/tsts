package com.aburv.takbuff.data

import android.os.StrictMode
import android.util.Log
import com.aburv.takbuff.BuildConfig
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import org.json.JSONException
import org.json.JSONObject
import java.io.IOException
import java.io.OutputStreamWriter
import java.net.ConnectException
import java.net.HttpURLConnection
import java.net.URL

open class APIRequest {
    companion object {
        const val DOMAIN: String = "${BuildConfig.API_DOMAIN}/api"
    }

    fun get(path: String, response: Response) {
        val url = URL("$DOMAIN/$path")
        val httpURLConnection = url.openConnection() as HttpURLConnection
        httpURLConnection.requestMethod = "GET"
        setHeaders(httpURLConnection)
        this.dataCall(httpURLConnection, response)
    }

    fun setHeaders(httpURLConnection: HttpURLConnection) {
        httpURLConnection.setRequestProperty(
            "x-api-key",
            BuildConfig.API_KEY
        )
        httpURLConnection.setRequestProperty(
            "x-access-key",
            ""
        )
        httpURLConnection.setRequestProperty(
            "Content-Type",
            "application/json"
        )
        httpURLConnection.setRequestProperty(
            "Accept",
            "application/json"
        )
    }

    fun post(path: String, data: JSONObject, response: Response) {
        val body = JSONObject()
        body.put("data", data)
        val dataString = body.toString()
        val url = URL("$DOMAIN/$path")
        val httpURLConnection = url.openConnection() as HttpURLConnection
        httpURLConnection.requestMethod = "POST"
        setHeaders(httpURLConnection)
        httpURLConnection.doInput = true
        httpURLConnection.doOutput = true
        val outputStreamWriter = OutputStreamWriter(httpURLConnection.outputStream)
        outputStreamWriter.write(dataString)
        outputStreamWriter.flush()
        this.dataCall(httpURLConnection, response)
    }

    @OptIn(DelicateCoroutinesApi::class)
    private fun dataCall(httpURLConnection: HttpURLConnection, response: Response) {
        val policy: StrictMode.ThreadPolicy = StrictMode.ThreadPolicy.Builder().permitAll().build()
        StrictMode.setThreadPolicy(policy)
        var responseDataText: String?
        GlobalScope.launch(Dispatchers.IO) {
            try {
                httpURLConnection.connect()
                val responseCode = httpURLConnection.responseCode
                if (responseCode == HttpURLConnection.HTTP_NOT_FOUND) {
                    ping()
                } else {
                    val responseText = httpURLConnection.inputStream.bufferedReader().readText()
                    responseDataText = try {
                        JSONObject(responseText).getJSONObject("data").toString()
                    } catch (e: JSONException) {
                        JSONObject(responseText).getString("data")
                    }
                    Log.i("API Request: success", responseDataText!!)
                    launch(Dispatchers.Main) {
                        response.onData(responseDataText!!)
                    }
                }
            } catch (e: ConnectException) {
                launch(Dispatchers.Main) {
                    response.onError("Connection error $e")
                }
            } catch (e: IOException) {
                launch(Dispatchers.Main) {
                    response.onError("IO error $e")
                }
            } catch (e: Exception) {
                launch(Dispatchers.Main) {
                    response.onError("Error $e")
                }
            }
        }
    }

    @OptIn(DelicateCoroutinesApi::class)
    fun ping() {
        GlobalScope.launch(Dispatchers.IO) {
            try {
                val url = URL("$DOMAIN/ping/")
                val httpURLConnection = url.openConnection() as HttpURLConnection
                httpURLConnection.requestMethod = "POST"
                httpURLConnection.setRequestProperty(
                    "x-api-key",
                    BuildConfig.API_KEY
                )
                httpURLConnection.connect()
                val responseCode = httpURLConnection.responseCode
                if (responseCode == HttpURLConnection.HTTP_NOT_FOUND) {
                    // emit a no internet call
                    Log.e("set server down", "")
                }
            } catch (e: ConnectException) {
                Log.e("API Request: Connection error", e.toString())
            } catch (e: IOException) {
                Log.e("API Request: IO error", e.toString())
            } catch (e: Exception) {
                Log.e("API Request: others", e.toString())
            }
        }
    }
}

interface Response {
    fun onData(value: String)
    fun onError(value: String)
}