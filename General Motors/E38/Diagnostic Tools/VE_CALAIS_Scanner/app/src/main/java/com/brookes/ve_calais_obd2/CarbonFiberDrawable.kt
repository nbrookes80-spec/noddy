package com.brookes.ve_calais_obd2

import android.graphics.Bitmap
import android.graphics.BitmapShader
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.ColorFilter
import android.graphics.Paint
import android.graphics.PixelFormat
import android.graphics.Shader
import android.graphics.drawable.Drawable

/**
 * Procedural carbon-fibre weave texture, generated at runtime instead of shipped as a raster
 * asset - there's no licensed carbon-fibre photo/texture to bundle, and this gives an identical
 * result at zero APK size cost. Draws one small basket-weave tile into an offscreen bitmap once,
 * then paints it across the drawable's bounds via a repeating BitmapShader.
 */
class CarbonFiberDrawable(
    private val baseColor: Int = Color.parseColor("#0D0D0D"),
    private val weaveColor: Int = Color.parseColor("#242424"),
    private val highlightColor: Int = Color.parseColor("#333333")
) : Drawable() {

    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private var shader: BitmapShader? = null

    private fun buildTile(): Bitmap {
        val tileSize = 28
        val bmp = Bitmap.createBitmap(tileSize, tileSize, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(bmp)
        canvas.drawColor(baseColor)

        val cellPaint = Paint(Paint.ANTI_ALIAS_FLAG)
        val half = tileSize / 2f

        // Basket-weave: alternating cells swap which color is "up", the classic twill look.
        cellPaint.color = weaveColor
        canvas.drawRect(0f, 0f, half, half, cellPaint)
        canvas.drawRect(half, half, tileSize.toFloat(), tileSize.toFloat(), cellPaint)

        // Thin highlight lines across each cell suggest the fibre sheen catching light.
        cellPaint.color = highlightColor
        cellPaint.strokeWidth = 1.2f
        canvas.drawLine(0f, half / 2f, half, half / 2f, cellPaint)
        canvas.drawLine(half, tileSize - half / 2f, tileSize.toFloat(), tileSize - half / 2f, cellPaint)
        canvas.drawLine(half + half / 2f, 0f, half + half / 2f, half, cellPaint)
        canvas.drawLine(half / 2f, half, half / 2f, tileSize.toFloat(), cellPaint)

        return bmp
    }

    override fun draw(canvas: Canvas) {
        if (shader == null) {
            val tile = buildTile()
            shader = BitmapShader(tile, Shader.TileMode.REPEAT, Shader.TileMode.REPEAT)
            paint.shader = shader
        }
        canvas.drawRect(bounds, paint)
    }

    override fun setAlpha(alpha: Int) {
        paint.alpha = alpha
    }

    override fun setColorFilter(colorFilter: ColorFilter?) {
        paint.colorFilter = colorFilter
    }

    @Deprecated("Deprecated in Java", ReplaceWith("PixelFormat.OPAQUE"))
    override fun getOpacity(): Int = PixelFormat.OPAQUE
}
