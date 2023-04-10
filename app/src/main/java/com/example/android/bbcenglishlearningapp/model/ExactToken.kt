package com.example.android.bbcenglishlearningapp.model

class ExactToken(
    override val text: String,
    override val shape: TokenShape = TokenShape.Lowercase,
    override val extraBefore: String? = null,
    override val extraAfter: String? = null,
) : Token() {

    override fun hashCode(): Int {
        return this.toString().hashCode()
    }

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as ExactToken

        if (text != other.text) return false
        if (shape != other.shape) return false
        if (extraBefore != other.extraBefore) return false
        if (extraAfter != other.extraAfter) return false

        return true
    }
}