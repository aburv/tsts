package com.aburv.takbuff

import android.os.AsyncTask
import java.io.BufferedOutputStream
import java.io.OutputStream
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL


class DataSend : AsyncTask<String?, Int?, String?>() {
    override fun doInBackground(vararg params: String?): String? {
        val myUrl = params[0]
        val myData = params[1]
        try {
            val url = URL(myUrl)
            val httpURLConnection = url.openConnection() as HttpURLConnection
            httpURLConnection.requestMethod = "GET"
            httpURLConnection.setRequestProperty("Content-Type", "application/json")
            try {
                httpURLConnection.doOutput = true
                httpURLConnection.setChunkedStreamingMode(0)

                val outputStream: OutputStream =
                    BufferedOutputStream(httpURLConnection.outputStream)
                val outputStreamWriter = OutputStreamWriter(outputStream)
                outputStreamWriter.write(myData)
                outputStreamWriter.flush()
                outputStreamWriter.close()
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                httpURLConnection.disconnect()
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return null
    }
}