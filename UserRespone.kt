package com.example.myapplication.model

import com.google.gson.annotations.SerializedName


data class UsersResponse(
    @SerializedName("users") val users: List<User>
)

