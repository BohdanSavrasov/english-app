package com.example.android.bbcenglishlearningapp.model

class ParallelToken(val tokens: List<Token>) : Token() {
    override val text: String
        get() = tokens.first().text
    override val shape: TokenShape
        get() = tokens.first().shape
    override val extraBefore: String?
        get() = tokens.first().extraBefore
    override val extraAfter: String?
        get() = tokens.first().extraAfter

    override fun hashCode(): Int {
        return tokens.hashCode()
    }

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as ParallelToken

        if (tokens != other.tokens) return false

        return true
    }
}