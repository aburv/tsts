package com.aburv.takbuff.services

import android.content.Context
import android.util.Log
import androidx.credentials.Credential
import androidx.credentials.CredentialManager
import androidx.credentials.CustomCredential
import androidx.credentials.GetCredentialRequest
import androidx.credentials.GetCredentialResponse
import androidx.credentials.exceptions.GetCredentialException
import androidx.credentials.exceptions.NoCredentialException
import com.aburv.takbuff.BuildConfig
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.google.android.libraries.identity.googleid.GoogleIdTokenParsingException
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch


class GAuthService(private val context: Context) {
    companion object {
        private const val TAG = "App-GoogleAuthService"
    }

    fun auth(response: GoogleAuthResponse) {
        Log.i(TAG, "Google Login Call")
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val credentialManager = CredentialManager.create(context)

                val option = GetGoogleIdOption.Builder()
                    .setFilterByAuthorizedAccounts(false)
                    .setServerClientId(BuildConfig.G_CLIENT_ID)
                    .build()

                val request = GetCredentialRequest.Builder()
                    .addCredentialOption(option)
                    .build()

                val result = credentialManager.getCredential(
                    context = context,
                    request = request,
                )

                val googleIdTokenCredential = handleSignIn(result)
                launch(Dispatchers.Main) {
                    response.onUser(googleIdTokenCredential!!)
                }
            } catch (e: NoCredentialException) {
                Log.i(TAG, "NoCredentialException $e")
                response.onError("No Google user logged in")
            } catch (e: GetCredentialException) {
                Log.i(TAG, "GetCredentialException $e")
                response.onError("Unexpected Error on Google Login")
            } catch (e: Exception) {
                Log.i(TAG, "Exception $e")
                response.onError("Unexpected Error on Google Login ")
            }
        }
    }

    private fun handleSignIn(result: GetCredentialResponse): GoogleIdTokenCredential? {
        Log.i(TAG, "Handle Sign in")
        try {
            val credential: Credential = result.credential
            if (credential is CustomCredential && credential.type == GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL) {
                return GoogleIdTokenCredential.createFrom(credential.data)
            } else {
                Log.i(TAG, "Unexpected type of credential")
                return null
            }
        } catch (e: GoogleIdTokenParsingException) {
            Log.i(TAG, "Received an invalid google id token response", e)
            return null
        }
    }
}

interface GoogleAuthResponse {
    fun onUser(googleUser: GoogleIdTokenCredential)
    fun onError(message: String)
}

