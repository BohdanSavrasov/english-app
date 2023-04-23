package com.example.android.bbcenglishlearningapp.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.*
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.example.android.bbcenglishlearningapp.model.*
import com.example.android.bbcenglishlearningapp.ui.theme.BBCEnglishLearningAppTheme
import com.example.android.bbcenglishlearningapp.ui.theme.MainBackground


@Composable
fun MatchingScreen(testtext: String) {

    var model by remember { mutableStateOf(
        MatchingModel(
            listOf(
                ExactToken("amy", shape = TokenShape.Capitalized),
                ExactToken("is"),
                ExactToken("back"),
                ExactToken("home"),
                ExactToken("now", extraAfter = "."),
                ExactToken("she", shape = TokenShape.Capitalized),
                ParallelToken(
                    listOf(
                        ExactToken("is"),
                        ExactToken("are", shape = TokenShape.Lowercase),
                        SeqToken(
                            listOf(
                                ExactToken("has"),
                                ExactToken("been"),
                                ExactToken("to"),
                            )
                        ),
                        SeqToken(
                            listOf(
                                ExactToken("has"),
                                ExactToken("gone"),
                                ExactToken("to"),
                            )
                        ),
                    )
                ),
                ExactToken("italy", shape = TokenShape.Capitalized, extraAfter = "."),
            ),
            listOf(null),
        ))
    }

    BBCEnglishLearningAppTheme {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MainBackground)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            LinearProgressIndicator(
                modifier = Modifier.fillMaxWidth(),
                progress = .5f,
            )

            Spacer(modifier = Modifier.weight(1f))

            Text(testtext)

            MatchingLayout(
                model = model,
                onClick = { t ->
                    if (model.targets.indexOf(t) >= 0) {
                        model = model.copy(targets = emptyList())
                    } else {
                        model = model.copy(targets = listOf(t))
                    }
                },
            )

            Spacer(modifier = Modifier.weight(1f))

            Button(
                colors = ButtonDefaults.buttonColors(
                    backgroundColor = MaterialTheme.colors.surface,
                    contentColor = MaterialTheme.colors.primary,
                ),
                onClick = { /*TODO*/ },
                contentPadding = PaddingValues(horizontal = 48.dp, vertical = 18.dp),
                shape = MaterialTheme.shapes.medium,
            ) {
                Text(text = "Check my answer")
            }
        }
    }

}

sealed class MatchingRole {
    object Token : MatchingRole()
    object Target : MatchingRole()
    object BackDrop : MatchingRole()
    data class Option(
        val animationProgress: Double,
        val targetIndex: Int,
    ) : MatchingRole()
}

class MatchingDataModifier(
    val role: MatchingRole,
) : ParentDataModifier {
    override fun Density.modifyParentData(parentData: Any?): Any? = this@MatchingDataModifier
}

interface MatchingScope {
    @Stable
    fun Modifier.matchingRole(role: MatchingRole) = this.then(
        MatchingDataModifier(role)
    )

    companion object : MatchingScope
}

@Composable
fun MatchingLayout(
    modifier: Modifier = Modifier,
    horizontalSpace: Dp = 4.dp,
    verticalSpace: Dp = 4.dp,
    model: MatchingModel,
    onClick: (Token) -> Unit,
) {
    val mixedOptions = remember(model.tokens) {
        model.tokens
            .filterIsInstance<ParallelToken>()
            .flatMap { it.tokens }
            .shuffled()
    }

    val mixedOptionsState by remember(mixedOptions, model.targets) {
        derivedStateOf {
            mixedOptions.map { t ->
                val idx = model.targets.indexOf(t)
                if (idx < 0) {
                    Triple(t, 0.0, 0)
                } else {
                    Triple(t, 1.0, idx)
                }
            }
        }
    }

    val transition = updateTransition(mixedOptionsState, "Targets animation")

    val animatedMixedOptionsProgress = List(mixedOptionsState.size) { i ->
        transition.animateFloat(label = "") { triples ->
            triples[i].second.toFloat()
        }
    }

    val content: @Composable MatchingScope.() -> Unit = {
        model.tokens.forEach { token ->
            when (token) {
                is ExactToken -> {
                    Text(
                        modifier = Modifier.matchingRole(MatchingRole.Token),
                        text = token.toString(),
                        color = MaterialTheme.colors.onBackground,
                    )
                }
                is ParallelToken -> {
                    Spacer(
                        modifier = Modifier.matchingRole(MatchingRole.Target),
                    )
                }
            }
        }

        mixedOptionsState.forEachIndexed { i, (option, progress, targetIndex) ->
            Pill(
                modifier = Modifier.matchingRole(MatchingRole.Option(animatedMixedOptionsProgress[i].value.toDouble(), targetIndex)),
                text = option.toString(),
                onClick = { onClick(option) }
            )
            Pill(
                modifier = Modifier.matchingRole(MatchingRole.BackDrop),
                text = option.toString(),
                contourOnly = true,
            )
        }
    }

    data class Box(
        val m: Measurable,
        val p: Placeable,
        val r : MatchingRole,
        val x: Int,
        val y: Int,
        val width: Int,
        val height: Int,
        val altP: Placeable? = null,
    )

    class Row(
        val maxItemsCount: Int,
        val rowWidthLimitPx: Int,
        val horizontalSpacePx: Int,
    ) : Iterable<Box> {
        private val items = Array<Box?>(maxItemsCount) { null }
        private var idx = 0
        private var startPaddingPx = rowWidthLimitPx / 2
        private var rowWidthPx = 0
        private var rowHeightPx = 0

        fun width() = rowWidthPx

        fun height() = rowHeightPx

        fun add(b: Box): Boolean {
            if (idx >= maxItemsCount) {
                return false
            }

            if (rowWidthPx + horizontalSpacePx + b.width > rowWidthLimitPx) {
                return false
            }

            if (b.height > rowHeightPx) {
                rowHeightPx = b.height
            }

            items[idx] = b.copy(x = rowWidthPx)

            rowWidthPx += horizontalSpacePx + b.width

            startPaddingPx = ((rowWidthLimitPx / 2.0) - (rowWidthPx / 2.0)).toInt()

            idx += 1

            return true
        }

        override fun iterator() = object : Iterator<Box> {
            var i: Int = 0

            override fun hasNext(): Boolean = i < idx

            override fun next(): Box {
                val res = items[i]!!
                i += 1
                return res.copy(
                    x = startPaddingPx + res.x,
                    y = ((rowHeightPx / 2.0) - (res.height / 2.0)).toInt(),
                )
            }
        }

    }

    fun lerp(box: Box, target: Box, k: Double): Box {
        val targetX = (target.width / 2.0) - (box.width / 2.0) + target.x
        val targetY = (target.height / 2.0) - (box.height / 2.0) + target.y
        val xDiff = targetX - box.x
        val yDiff = targetY - box.y
        return box.copy(
            x = (xDiff * k + box.x).toInt(),
            y = (yDiff * k + box.y).toInt()
        )
    }

    Layout(
        modifier = modifier,
        content = { MatchingScope.content() },
        measurePolicy = { measureables, constr ->
            val horizontalSpacePx = horizontalSpace.roundToPx()
            val verticalSpacePx = verticalSpace.roundToPx()

            var boxes = measureables.map { m ->
                val p = m.measure(constr)
                Box(
                    m = m,
                    p = p,
                    r = (m.parentData as MatchingDataModifier).role,
                    x = 0,
                    y = 0,
                    width = p.width,
                    height = p.height
                )
            }

            val maxTargetWidthPx = boxes
                .filter { it.r is MatchingRole.Option }
                .maxOf { it.width }

            val maxTargetHeightPx = boxes
                .filter { it.r is MatchingRole.Option }
                .maxOf { it.height }

            boxes = boxes
                .map {
                    return@map if (it.r is MatchingRole.Target) {
                        it.copy(width = maxTargetWidthPx, height = maxTargetHeightPx)
                    } else it
                }
                .windowed(size = 2, step = 1, partialWindows = true) { list ->
                    if (list[0].r is MatchingRole.BackDrop) {
                        return@windowed null
                    }
                    if (list[0].r is MatchingRole.Option && list[1].r is MatchingRole.BackDrop) {
                        return@windowed list[0].copy(
                            altP = list[1].p
                        )
                    }
                    return@windowed list[0]
                }
                .filterNotNull()

            val mCount = measureables.size
            val topRows = mutableListOf(Row(mCount, constr.maxWidth, horizontalSpacePx))
            val btmRows = mutableListOf(Row(mCount, constr.maxWidth, horizontalSpacePx * 2))

            boxes.forEach { b ->
                when (b.r) {
                    MatchingRole.Token, MatchingRole.Target -> {
                        if (!topRows.last().add(b)) {
                            val newRow = Row(mCount, constr.maxWidth, horizontalSpacePx)
                            newRow.add(b)
                            topRows.add(newRow)
                        }
                    }
                    else -> {
                        if (!btmRows.last().add(b)) {
                            val newRow = Row(mCount, constr.maxWidth, horizontalSpacePx * 2)
                            newRow.add(b)
                            btmRows.add(newRow)
                        }
                    }
                }
            }

            val targets = topRows
                .flatten()
                .filter { it.r is MatchingRole.Target }
                .toList()

            val gap = 64.dp.roundToPx()

            val actualHeight = gap +
                    topRows.sumOf { it.height() } + (topRows.size - 1) * verticalSpacePx +
                    btmRows.sumOf { it.height() } + (btmRows.size) * verticalSpacePx

            layout(constr.maxWidth, actualHeight) {
                var rowY = 0
                topRows.forEach { row ->
                    row.forEach { b ->
                        b.p.place(b.x, rowY + b.y)
                    }
                    rowY += row.height() + verticalSpacePx
                }

                rowY += gap

                btmRows.forEach { row ->
                    row.forEach { b ->
                        val box = b.copy(y = b.y + rowY)

                        if (box.altP != null && box.r is MatchingRole.Option && box.r.animationProgress > 0) {
                            val lrp = lerp(box, targets[0], box.r.animationProgress)
                            box.altP.place(box.x, box.y, 0f)
                            box.p.place(lrp.x, lrp.y, 1f)
                        } else {
                            box.p.place(box.x, box.y)
                        }
                    }
                    rowY += row.height() + verticalSpacePx
                }
            }
        }
    )

}

@Composable
@Preview(showBackground = true)
fun previewMatchingLayout() {
    val model = MatchingModel(
        listOf(
            ExactToken("amy", shape = TokenShape.Capitalized),
            ExactToken("is"),
            ExactToken("back"),
            ExactToken("home"),
            ExactToken("now", extraAfter = "."),
            ExactToken("she", shape = TokenShape.Capitalized),
            ParallelToken(
                listOf(
                    ExactToken("is"),
                    ExactToken("are"),
                    SeqToken(
                        listOf(
                            ExactToken("has"),
                            ExactToken("been"),
                            ExactToken("to"),
                        )
                    ),
                    SeqToken(
                        listOf(
                            ExactToken("has"),
                            ExactToken("gone"),
                            ExactToken("to"),
                        )
                    ),
                )
            ),
            ExactToken("italy", shape = TokenShape.Capitalized, extraAfter = "."),
        ),
        emptyList(),
    )

    BBCEnglishLearningAppTheme {
        MatchingLayout(
            modifier = Modifier.background(MainBackground),
            model = model,
            onClick = {}
        )
    }
}
