package com.example.android.bbcenglishlearningapp.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.example.android.bbcenglishlearningapp.R

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val xmlParser = resources.getXml(R.xml.tasks)
        xmlParser


        setContent { MatchingScreen(tasksRes.name) }
    }
}