package com.example.schooldefmobile.login

import com.android.volley.Request
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.example.schooldefmobile.profile.ProfileActivity
import com.example.schooldefmobile.R
import org.json.JSONObject
import com.android.volley.Request.Method


class LoginActivity : AppCompatActivity() {

    private val LOGIN_URL = "http://10.0.2.2:8000/api/token/"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val emailEditText = findViewById<EditText>(R.id.emailEditText)
        val passwordEditText = findViewById<EditText>(R.id.passwordEditText)
        val loginButton = findViewById<Button>(R.id.loginButton)

        loginButton.setOnClickListener {
            val email = emailEditText.text.toString()
            val password = passwordEditText.text.toString()
            login(email, password)
        }
    }

    private fun login(email: String, password: String) {
        val json = JSONObject()
        json.put("email", email)
        json.put("password", password)

        val requestQueue = Volley.newRequestQueue(this)
        val request = JsonObjectRequest(Request.Method.POST, LOGIN_URL, json,
            { response ->
                val accessToken = response.getString("access")

                val prefs = getSharedPreferences("MyAppPrefs", MODE_PRIVATE)
                prefs.edit().putString("access_token", accessToken).apply()

                Toast.makeText(this, "Успешный вход!", Toast.LENGTH_SHORT).show()
                startActivity(Intent(this, ProfileActivity::class.java))
                finish()
            },
            { error ->
                Toast.makeText(this, "Ошибка: ${error.message}", Toast.LENGTH_SHORT).show()
            })
        requestQueue.add(request)
    }
}