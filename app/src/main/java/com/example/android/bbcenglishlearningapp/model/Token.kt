package com.example.android.bbcenglishlearningapp.model

import androidx.compose.ui.text.capitalize
import androidx.compose.ui.text.intl.Locale

abstract class Token {
    abstract val text: String
    abstract val shape: TokenShape
    abstract val extraBefore: String?
    abstract val extraAfter: String?

    override fun toString(): String {
        val sb = StringBuilder()

        extraBefore?.let { sb.append(it) }

        sb.append(when (shape) {
            TokenShape.Lowercase -> text.lowercase()
            TokenShape.Uppercase -> text.uppercase()
            TokenShape.Capitalized -> text.capitalize(Locale.current)
        })

        extraAfter?.let { sb.append(it) }

        return sb.toString()
    }

    fun size() = this.toString().length
}