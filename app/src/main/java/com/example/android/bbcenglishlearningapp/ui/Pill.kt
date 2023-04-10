package com.example.android.bbcenglishlearningapp.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.padding
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.example.android.bbcenglishlearningapp.ui.theme.Shapes

@Composable
fun Pill(
    modifier: Modifier = Modifier,
    text: String,
    contourOnly: Boolean = false,
    onClick: () -> Unit = {},
) {
    if (contourOnly) {
        Surface(
            modifier = modifier,
            shape = Shapes.small,
            color = Color.Transparent,
            border = BorderStroke(1.dp, MaterialTheme.colors.surface),
            elevation = 0.dp,
        ) {
            Text(
                modifier = Modifier
                    .padding(horizontal = 8.dp, vertical = 4.dp)
                    .alpha(0f),
                text = text,
            )
        }
    } else {
        Surface(
            modifier = modifier.then(
                Modifier.clickable(onClick = onClick)
            ),
            shape = Shapes.small,
            color = MaterialTheme.colors.surface,
            elevation = 1.dp,
        ) {
            Text(
                modifier = Modifier
                    .padding(horizontal = 8.dp, vertical = 4.dp),
                text = text,
            )
        }
    }
}