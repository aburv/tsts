package com.aburv.takbuff.data

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import com.aburv.takbuff.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.security.KeyPairGenerator
import java.security.KeyStore
import java.security.PrivateKey
import java.security.Signature
import java.security.spec.ECGenParameterSpec
import java.util.UUID

class ClientIdentity(private val context: Context) {
    companion object {
        const val PLATFORM = "android"
        private const val PREFERENCES = "client_identity"
        private const val INSTALLATION_ID = "installation_id"
        private const val CLIENT_TOKEN = "client_token"
        private const val CLIENT_TOKEN_EXPIRES_AT = "client_token_expires_at"
        private const val KEY_ALIAS = "takbuff_client_identity"
        private val bootstrapMutex = Mutex()
    }

    suspend fun getClientToken(): String = bootstrapMutex.withLock {
        val preferences = context.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE)
        val existing = preferences.getString(CLIENT_TOKEN, null)
        val expiresAt = preferences.getLong(CLIENT_TOKEN_EXPIRES_AT, 0L)
        if (!existing.isNullOrBlank() && expiresAt > System.currentTimeMillis() / 1000 + 60) {
            return@withLock existing
        }
        val installationId = getInstallationId()
        val publicKey = getOrCreateKeyPair()
        val challenge = requestChallenge(installationId, publicKey)
        val signature = sign(challenge)
        val session = createSession(installationId, challenge, signature)
        preferences.edit()
            .putString(CLIENT_TOKEN, session.first)
            .putLong(CLIENT_TOKEN_EXPIRES_AT, session.second)
            .apply()
        session.first
    }

    fun getInstallationId(): String {
        val preferences = context.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE)
        return preferences.getString(INSTALLATION_ID, null)
            ?: UUID.randomUUID().toString().replace("-", "").also {
                preferences.edit().putString(INSTALLATION_ID, it).apply()
            }
    }

    fun signRequest(payload: String): String = sign(payload)

    private fun getOrCreateKeyPair(): String {
        val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        if (!keyStore.containsAlias(KEY_ALIAS)) {
            KeyPairGenerator.getInstance("EC", "AndroidKeyStore").apply {
                initialize(
                    KeyGenParameterSpec.Builder(
                        KEY_ALIAS,
                        KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY
                    )
                        .setAlgorithmParameterSpec(ECGenParameterSpec("secp256r1"))
                        .setDigests(KeyProperties.DIGEST_SHA256)
                        .build()
                )
                generateKeyPair()
            }
        }
        val certificate = keyStore.getCertificate(KEY_ALIAS)
            ?: throw IllegalStateException("Client key was not created")
        return Base64.encodeToString(certificate.publicKey.encoded, Base64.NO_WRAP)
    }

    private fun sign(payload: String): String {
        val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        val privateKey = keyStore.getKey(KEY_ALIAS, null) as? PrivateKey
            ?: throw IllegalStateException("Client private key was not found")
        return Base64.encodeToString(
            Signature.getInstance("SHA256withECDSA").run {
                initSign(privateKey)
                update(payload.toByteArray(Charsets.UTF_8))
                sign()
            },
            Base64.NO_WRAP
        )
    }

    private suspend fun requestChallenge(installationId: String, publicKey: String): String =
        withContext(Dispatchers.IO) {
            val connection = openConnection("client/challenge")
            val body = JSONObject().put(
                "data", JSONObject()
                    .put("installationId", installationId)
                    .put("publicKey", publicKey)
                    .put("platform", PLATFORM)
            ).toString()
            connection.outputStream.bufferedWriter().use { it.write(body) }
            readData(connection, "challenge")
        }

    private suspend fun createSession(
        installationId: String,
        challenge: String,
        signature: String
    ): Pair<String, Long> = withContext(Dispatchers.IO) {
        val connection = openConnection("client/session")
        val body = JSONObject().put(
            "data", JSONObject()
                .put("installationId", installationId)
                .put("platform", PLATFORM)
                .put("challenge", challenge)
                .put("signature", signature)
        ).toString()
        connection.outputStream.bufferedWriter().use { it.write(body) }
        if (connection.responseCode !in 200..299) {
            throw IllegalStateException("Client session failed: ${connection.responseCode}")
        }
        val data = JSONObject(connection.inputStream.bufferedReader().use { it.readText() })
            .getJSONObject("data")
        Pair(data.getString("clientToken"), data.getLong("expiresAt"))
    }

    private fun openConnection(path: String): HttpURLConnection =
        (URL("${BuildConfig.API_DOMAIN}/api/$path").openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            doOutput = true
            setRequestProperty("Content-Type", "application/json")
        }

    private fun readData(connection: HttpURLConnection, key: String): String {
        if (connection.responseCode !in 200..299) {
            throw IllegalStateException("Client challenge failed: ${connection.responseCode}")
        }
        return JSONObject(connection.inputStream.bufferedReader().use { it.readText() })
            .getJSONObject("data")
            .getString(key)
    }
}
