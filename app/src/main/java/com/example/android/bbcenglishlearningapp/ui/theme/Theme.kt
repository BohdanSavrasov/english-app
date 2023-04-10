package com.example.android.bbcenglishlearningapp.ui.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.Colors
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Shapes
import androidx.compose.material.Typography
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.android.bbcenglishlearningapp.R

val Shapes = Shapes(
    small = RoundedCornerShape(16.dp),
    medium = RoundedCornerShape(24.dp),
    large = RoundedCornerShape(0.dp)
)

val BBCReithSans = FontFamily(
    Font(R.font.bbcreithsans_lt, FontWeight.Light, FontStyle.Normal),
    Font(R.font.bbcreithsans_ltit, FontWeight.Light, FontStyle.Italic),
    Font(R.font.bbcreithsans_rg, FontWeight.Normal, FontStyle.Normal),
    Font(R.font.bbcreithsans_md, FontWeight.Medium, FontStyle.Normal),
    Font(R.font.bbcreithsans_mdit, FontWeight.Medium, FontStyle.Italic),
    Font(R.font.bbcreithsans_bd, FontWeight.Bold, FontStyle.Normal),
    Font(R.font.bbcreithsans_bdit, FontWeight.Bold, FontStyle.Italic),
    Font(R.font.bbcreithsans_exbd, FontWeight.ExtraBold, FontStyle.Normal),
    Font(R.font.bbcreithsans_exbdit, FontWeight.ExtraBold, FontStyle.Italic),
)

val Typography = Typography(
    body1 = TextStyle(
        fontFamily = BBCReithSans,
        fontWeight = FontWeight.Bold,
        fontSize = 20.sp
    ),
    button = TextStyle(
        fontFamily = BBCReithSans,
        fontWeight = FontWeight.Medium,
        fontSize = 20.sp
    )
)

val Colors = Colors(
    primary = Color(0xFF08838B),
    primaryVariant = Color.Black,
    secondary = Color.Black,
    secondaryVariant = Color.Black,
    background = Color.Black,
    surface = Color.White,
    error = Color.Black,
    onPrimary = Color.Black,
    onSecondary = Color.Black,
    onBackground = Color.White,
    onSurface = Color.Black,
    onError = Color.Black,
    isLight = true,
)

val MainBackground = Brush.verticalGradient(
    listOf(Color(0xFF13399A), Color(0xFF08838B)),
)

@Composable
fun BBCEnglishLearningAppTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colors = Colors,
        typography = Typography,
        shapes = Shapes,
        content = content
    )
}