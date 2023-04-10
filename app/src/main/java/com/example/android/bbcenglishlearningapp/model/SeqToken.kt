package com.example.android.bbcenglishlearningapp.model

class SeqToken(val tokens: List<Token>): Token() {
    override val text: String
        get() {
            val sb = StringBuilder()

            for ((i, token) in tokens.withIndex()) {
                val isFirst = i == 0
                val isLast = i == tokens.size - 1

                if (!isFirst) {
                    token.extraBefore?.let { sb.append(it) }
                }

                sb.append(token.text)

                if (!isLast) {
                    token.extraAfter?.let { sb.append(it) }
                    sb.append(" ")
                }
            }

            return sb.toString()
        }

    override val shape: TokenShape
        get() = tokens.first().shape

    override val extraBefore: String?
        get() = tokens.first().extraBefore

    override val extraAfter: String?
        get() = tokens.last().extraAfter

    override fun hashCode(): Int {
        return tokens.hashCode()
    }

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as SeqToken

        if (tokens != other.tokens) return false

        return true
    }
}