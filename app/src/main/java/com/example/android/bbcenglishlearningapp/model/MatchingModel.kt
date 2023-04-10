package com.example.android.bbcenglishlearningapp.model

data class MatchingModel(
    val tokens: List<Token>,
    val targets: List<Token?>,
) {

    override fun toString(): String {
        val sb = StringBuilder()
        for (i in tokens.indices) {
            sb.append(tokens[i])
            if (i < tokens.size - 1) {
                sb.append(" ")
            }
        }
        return sb.toString()
    }
}