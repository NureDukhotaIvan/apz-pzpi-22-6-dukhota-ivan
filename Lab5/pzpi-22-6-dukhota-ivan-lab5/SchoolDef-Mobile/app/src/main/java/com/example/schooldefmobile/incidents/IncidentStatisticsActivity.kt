package com.example.schooldefmobile.incidents

import android.app.DownloadManager
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.example.schooldefmobile.R
import org.json.JSONObject
import com.android.volley.Request

class IncidentStatisticsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_incident_statistics)

        val prefs = getSharedPreferences("MyAppPrefs", MODE_PRIVATE)
        val token = prefs.getString("access_token", null)

        if (token == null) {
            Toast.makeText(this, "Помилка авторизації: токен відсутній", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        val totalIncidentsTextView = findViewById<TextView>(R.id.totalIncidentsTextView)
        val avgCountTextView = findViewById<TextView>(R.id.avgCountTextView)
        val severityTextView = findViewById<TextView>(R.id.severityTextView)
        val categoriesTextView = findViewById<TextView>(R.id.categoriesTextView)
        val backButton = findViewById<Button>(R.id.backButton)

        backButton.setOnClickListener {
            finish()
        }

        val url = "http://10.0.2.2:8000/api/blogic/incident-stats/"

        val request = object : StringRequest(
            Request.Method.GET, url,
            Response.Listener { response ->
                try {
                    val json = JSONObject(response)
                    totalIncidentsTextView.text = "Всього інцидентів: ${json.getInt("total_incidents")}"
                    avgCountTextView.text = "Середня кількість на день: ${json.getDouble("avg_count_per_day")}"

                    val severity = json.getJSONObject("severity")
                    severityTextView.text = """
                        Серйозність:
                          Мін: ${severity.getInt("min")}
                          Макс: ${severity.getInt("max")}
                          Середнє: ${severity.getDouble("avg")}
                    """.trimIndent()

                    val categoriesArray = json.getJSONArray("categories")
                    val categoriesText = StringBuilder()
                    for (i in 0 until categoriesArray.length()) {
                        val item = categoriesArray.getJSONObject(i)
                        categoriesText.append("  ${item.getString("type")}: ${item.getInt("count")}\n")
                    }
                    categoriesTextView.text = "Категорії:\n$categoriesText"
                } catch (e: Exception) {
                    Toast.makeText(this, "Помилка обробки даних", Toast.LENGTH_SHORT).show()
                }
            },
            Response.ErrorListener { error ->
                val errorMsg = error.networkResponse?.statusCode?.let { "Код $it" } ?: "Невідома помилка"
                Toast.makeText(this, "Помилка завантаження статистики: $errorMsg", Toast.LENGTH_SHORT).show()
            }
        ) {
            override fun getHeaders(): Map<String, String> {
                return mapOf("Authorization" to "Bearer $token")
            }
        }

        Volley.newRequestQueue(this).add(request)
    }
}