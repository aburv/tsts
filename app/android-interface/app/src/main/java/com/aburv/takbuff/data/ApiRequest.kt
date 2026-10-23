package com.aburv.takbuff.data

import android.content.Context
import android.os.StrictMode
import android.util.Log
import com.aburv.takbuff.BuildConfig
import com.aburv.takbuff.db.UserTokenDB
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONException
import org.json.JSONObject
import java.io.IOException
import java.io.OutputStream
import java.io.OutputStreamWriter
import java.net.ConnectException
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest
import java.util.UUID


open class APIRequest(private val context: Context) {
    companion object {
        private const val TAG = "App-Request"
        internal const val DOMAIN = "${BuildConfig.API_DOMAIN}/api"
    }

    suspend fun get(path: String, response: Response) {
        Log.i(TAG, "Get $path")
        val url = URL("$DOMAIN/$path")
        val httpURLConnection = withContext(Dispatchers.IO) {
            url.openConnection()
        } as HttpURLConnection
        httpURLConnection.requestMethod = "GET"
        setHeaders(httpURLConnection)
        this.dataCall(httpURLConnection, response)
    }

    suspend fun setHeaders(httpURLConnection: HttpURLConnection, body: ByteArray = ByteArray(0)) {
        Log.i(TAG, "Set headers")

        val userTokens = UserTokenDB(context).getUserToken()
        val accessToken = if (userTokens.isNotEmpty()) {
            userTokens[0].idToken + BuildConfig.SEPARATOR + userTokens[0].accessToken
        } else {
            ""
        }

        val identity = ClientIdentity(context)
        val token = identity.getClientToken()
        val timestamp = (System.currentTimeMillis() / 1000).toString()
        val requestId = UUID.randomUUID().toString()
        val bodyHash = MessageDigest.getInstance("SHA-256").digest(body)
            .joinToString("") { "%02x".format(it) }
        val canonical = listOf(
            httpURLConnection.requestMethod,
            httpURLConnection.url.path,
            timestamp,
            requestId,
            bodyHash,
            ClientIdentity.PLATFORM,
            identity.getInstallationId(),
        ).joinToString("\n")
        httpURLConnection.setRequestProperty(
            "x-api-key", 
            "Client $token"
        )
        httpURLConnection.setRequestProperty(
            "X-Client-Installation", 
            identity.getInstallationId()
        )
        httpURLConnection.setRequestProperty(
            "X-Client-Platform", 
            ClientIdentity.PLATFORM
        )
        httpURLConnection.setRequestProperty(
            "X-Client-Timestamp", 
            timestamp
        )
        httpURLConnection.setRequestProperty(
            "X-Client-Request-Id", 
            requestId
        )
        httpURLConnection.setRequestProperty(
            "X-Client-Signature", 
            identity.signRequest(canonical)
        )
        if (accessToken.isNotEmpty()) {
            httpURLConnection.setRequestProperty(
                "x-access-key",
                accessToken
            )
        }
        httpURLConnection.setRequestProperty(
            "Content-Type",
            "application/json"
        )
        httpURLConnection.setRequestProperty(
            "Accept",
            "application/json"
        )
    }

    suspend fun post(
        path: String,
        data: JSONObject,
        response: Response,
        transformDataString: (JSONObject) -> String = { it.toString() }
    ) {
        val body = JSONObject()
        body.put("data", data)
        val dataString = transformDataString(body)
        val url = URL("$DOMAIN/$path")
        val httpURLConnection = withContext(Dispatchers.IO) {
            url.openConnection()
        } as HttpURLConnection
        httpURLConnection.requestMethod = "POST"
        setHeaders(httpURLConnection, dataString.toByteArray(Charsets.UTF_8))
        httpURLConnection.doInput = true
        httpURLConnection.doOutput = true
        val outputStreamWriter = OutputStreamWriter(httpURLConnection.outputStream)
        withContext(Dispatchers.IO) {
            outputStreamWriter.write(dataString)
            outputStreamWriter.flush()
        }
        this.dataCall(httpURLConnection, response)
    }

    suspend fun upload(
        path: String,
        fileName: String,
        content: ByteArray,
        response: Response
    ) {
        val boundary = "----Takbuff${UUID.randomUUID()}"
        val body = buildMultipartBody(boundary, fileName, content)
        val url = URL("$DOMAIN/$path")
        val connection = withContext(Dispatchers.IO) {
            url.openConnection()
        } as HttpURLConnection
        connection.requestMethod = "POST"
        connection.doInput = true
        connection.doOutput = true
        setHeaders(connection)
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=$boundary")
        withContext(Dispatchers.IO) {
            connection.outputStream.use { output: OutputStream -> output.write(body) }
        }
        dataCall(connection, response)
    }

    private fun buildMultipartBody(boundary: String, fileName: String, content: ByteArray): ByteArray {
        val prefix = "--$boundary\r\n" +
            "Content-Disposition: form-data; name=\"file\"; filename=\"$fileName\"\r\n" +
            "Content-Type: image/jpeg\r\n\r\n"
        val suffix = "\r\n--$boundary--\r\n"
        return prefix.toByteArray(Charsets.UTF_8) + content + suffix.toByteArray(Charsets.UTF_8)
    }

    @OptIn(DelicateCoroutinesApi::class)
    private fun dataCall(httpURLConnection: HttpURLConnection, response: Response) {
        Log.i(TAG, "Data call")
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
                    } catch (_: JSONException) {
                        JSONObject(responseText).getString("data")
                    }
                    Log.i("API Request: success", responseDataText!!)
                    launch(Dispatchers.Main) {
                        response.onData(responseDataText)
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
            Log.i(TAG, "Ping call")
            try {
                val url = URL("$DOMAIN/ping/")
                val httpURLConnection = url.openConnection() as HttpURLConnection
                httpURLConnection.requestMethod = "POST"
                setHeaders(httpURLConnection)
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