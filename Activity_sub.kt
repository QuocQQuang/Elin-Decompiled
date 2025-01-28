package com.example.myapplication.activity

import android.content.Intent
import android.content.SharedPreferences
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.example.myapplication.*
import com.example.myapplication.model.*

import com.example.myapplication.adapter.StudentAdapter
import com.example.myapplication.databinding.ActivitySubBinding
import com.example.myapplication.model.User
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import android.widget.TextView

class activity_sub : AppCompatActivity() {
    private lateinit var binding: ActivitySubBinding
    private lateinit var apiService: ApiService
    private lateinit var studentAdapter: StudentAdapter
    private lateinit var sharedPref: SharedPreferences
    private var isSubmitted: Boolean = true // Mặc định hiển thị học sinh đã nộp

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySubBinding.inflate(layoutInflater)
        setContentView(binding.root)
        sharedPref = getSharedPreferences("user_data", MODE_PRIVATE)
        if (!Utils.isOnline(this)) {
            AlertDialog.Builder(this)
                .setTitle(application.getString(R.string.app_name))
                .setMessage("Thiết bị của bạn không kết nối với Internet!")
                .setCancelable(false)
                .setPositiveButton("OK") { dialog, _ ->
                    dialog.dismiss()
                    finish()
                }
                .show()
        }


        val postId = intent.getStringExtra("postId")
        isSubmitted = intent.getBooleanExtra("isSubmitted", true) // Mặc định là true nếu không có dữ liệu từ Intent
        val maxTitleLength = 10

        val retrofit = ApiClient.instance
        apiService = retrofit.create(ApiService::class.java)

        fetchStudentsBySubmissionStatus(postId.toString())


        binding.back.setOnClickListener {
            finish()
        }
    }

    private fun fetchStudentsBySubmissionStatus(postId: String) {
        Log.d("ActivitySub", "Fetching students for postId: $postId") // Thêm log hiển thị postId

        val call = if (isSubmitted) {
            apiService.getSubmittedUsers(postId)
        } else {
            apiService.getNotSubmittedUsers(postId)
        }

        call.enqueue(object : Callback<UsersResponse> { // Thay đổi từ List<User> thành UsersResponse
            override fun onResponse(call: Call<UsersResponse>, response: Response<UsersResponse>) {
                if (response.isSuccessful) {
                    val usersResponse = response.body()
                    usersResponse?.let {
                        val title = if (isSubmitted) "Học sinh dã nộp" else "Học sinh chưa nộp"
                        findViewById<TextView>(R.id.isSubb).text = title

                        val students = it.users // Truy cập mảng users từ đối tượng UsersResponse
                        studentAdapter = StudentAdapter(this@activity_sub, R.layout.list_sub, students)
                        binding.listStudentSub.adapter = studentAdapter
                    }
                } else {
                    handleResponseError(response.code())
                }
            }

            override fun onFailure(call: Call<UsersResponse>, t: Throwable) {
                Log.e("ActivitySub", "Lỗi khi hiển thị học sinh: $t")
                Toast.makeText(this@activity_sub, "Hiện không có học sinh nào!", Toast.LENGTH_SHORT).show()
            }
        })
    }


    private fun handleResponseError(code: Int) {
        when (code) {
            404 -> {
                Toast.makeText(this@activity_sub, "Không tìm thấy học sinh!", Toast.LENGTH_SHORT).show()
            }
            else -> {
                Log.e("ActivitySub", "Lỗi khi hiển thị học sinh: $code")
                Toast.makeText(this@activity_sub, "Hiện không có học sinh nào!", Toast.LENGTH_SHORT).show()
            }
        }
    }


}
