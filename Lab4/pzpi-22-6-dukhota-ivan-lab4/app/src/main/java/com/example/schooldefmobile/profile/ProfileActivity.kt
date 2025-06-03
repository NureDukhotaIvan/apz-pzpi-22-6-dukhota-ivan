package com.example.schooldefmobile.profile

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.toolbox.JsonArrayRequest
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.example.schooldefmobile.incidents.IncidentStatisticsActivity
import com.example.schooldefmobile.login.LoginActivity
import com.example.schooldefmobile.R

class ProfileActivity : AppCompatActivity() {

    private val PROFILE_URL = "http://10.0.2.2:8000/api/user/users/me/"
    private val NOTIFICATIONS_URL = "http://10.0.2.2:8000/api/action/notif/latest/"
    private lateinit var notificationTextView: TextView
    private val handler = Handler(Looper.getMainLooper())
    private val pollingInterval = 1_000L

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profile)

        val prefs = getSharedPreferences("MyAppPrefs", MODE_PRIVATE)
        val token = prefs.getString("access_token", null)

        if (token == null) {
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
            return
        }

        val nameTextView = findViewById<TextView>(R.id.fullNameTextView)
        val birthTextView = findViewById<TextView>(R.id.birthDateTextView)
        val emailTextView = findViewById<TextView>(R.id.emailTextView)
        val classTextView = findViewById<TextView>(R.id.classTextView)
        val logoutButton = findViewById<Button>(R.id.logoutButton)
        val emergencyButton = findViewById<Button>(R.id.actionNotificationButton)
        val statsButton = findViewById<Button>(R.id.viewStatisticsButton)
        notificationTextView = findViewById(R.id.notificationPlaceholder)

        val request = object : JsonObjectRequest(
            Request.Method.GET, PROFILE_URL, null,
            { response ->
                val role = response.getString("role")
                if (role == "student") {
                    val student = response.getJSONObject("student_details")
                    val fullName = "${student.getString("first_name")} ${student.getString("last_name")}"
                    nameTextView.text = fullName
                    birthTextView.text = "Дата народження: ${student.getString("date_of_birth")}"
                    emailTextView.text = "Email: ${student.getString("email")}"
                    classTextView.text = "Клас: ${student.getString("student_class")}"
                }
            },
            { error ->
                Toast.makeText(this, "Ошибка загрузки профиля: ${error.message}", Toast.LENGTH_SHORT).show()
            }
        ) {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
                headers["Authorization"] = "Bearer $token"
                return headers
            }
        }

        Volley.newRequestQueue(this).add(request)

        logoutButton.setOnClickListener {
            prefs.edit().clear().apply()
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }

        emergencyButton.setOnClickListener {
            val emergencyUrl = "http://10.0.2.2:8000/api/action/emergency/"
            val queue = Volley.newRequestQueue(this)
            val jsonRequest = object : JsonObjectRequest(
                Method.POST, emergencyUrl, null,
                { _ ->
                    Toast.makeText(this, "Екстрена дія відправлена", Toast.LENGTH_SHORT).show()
                },
                { error ->
                    Toast.makeText(this, "Помилка відправки: ${error.message}", Toast.LENGTH_SHORT).show()
                }
            ) {
                override fun getHeaders(): MutableMap<String, String> {
                    val headers = HashMap<String, String>()
                    headers["Authorization"] = "Bearer $token"
                    return headers
                }
            }
            queue.add(jsonRequest)
        }

        statsButton.setOnClickListener {
            val intent = Intent(this, IncidentStatisticsActivity::class.java)
            startActivity(intent)
        }

        startNotificationPolling(token)
    }

    private fun startNotificationPolling(token: String) {
        val queue = Volley.newRequestQueue(this)

        val runnable = object : Runnable {
            override fun run() {
                val jsonArrayRequest = object : JsonArrayRequest(
                    Method.GET,
                    NOTIFICATIONS_URL,
                    null,
                    { response ->
                        if (response.length() > 0) {
                            val notification = response.getJSONObject(0)
                            val description = notification.getString("description")
                            notificationTextView.text = description
                        } else {
                            notificationTextView.text = "Нових повідомлень немає"
                        }
                    },
                    { error ->
                    }
                ) {
                    override fun getHeaders(): MutableMap<String, String> {
                        return hashMapOf("Authorization" to "Bearer $token")
                    }
                }

                queue.add(jsonArrayRequest)
                handler.postDelayed(this, pollingInterval)
            }
        }

        handler.post(runnable)
    }

    override fun onDestroy() {
        super.onDestroy()
        handler.removeCallbacksAndMessages(null)
    }
}