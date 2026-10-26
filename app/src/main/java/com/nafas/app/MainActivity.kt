package com.nafas.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val Ink = Color(0xFF100D20)
private val Violet = Color(0xFF8B5CF6)
private val Pink = Color(0xFFFF4FA3)
private val Muted = Color(0xFFB9B2D0)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                NafasHome()
            }
        }
    }
}

@Composable
private fun NafasHome() {
    Surface(modifier = Modifier.fillMaxSize(), color = Ink) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    Brush.verticalGradient(
                        listOf(Color(0xFF20123B), Ink, Color(0xFF090813))
                    )
                )
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(18.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text("نَفَس", color = Color.White, fontSize = 32.sp, fontWeight = FontWeight.ExtraBold)
                    Text("صوتك.. عالمك", color = Muted, fontSize = 14.sp)
                }
                Box(
                    modifier = Modifier
                        .background(Violet.copy(alpha = 0.22f), RoundedCornerShape(18.dp))
                        .padding(horizontal = 14.dp, vertical = 10.dp)
                ) {
                    Text("✦ VIP", color = Color(0xFFFFD66B), fontWeight = FontWeight.Bold)
                }
            }

            Text("اكتشف غرفًا تناسب مزاجك", color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Bold)
            Text("غرف مباشرة • مجتمعات • أصدقاء", color = Muted, fontSize = 14.sp)

            RoomCard("ليالي السمر", "دردشة وأصدقاء", "● مباشر الآن", Violet)
            RoomCard("مساحة الموسيقى", "استمع وشارك الحديث", "٨ متحدثين", Pink)
            RoomCard("قهوة الصباح", "تعارف وحديث لطيف", "١٢ مستمعًا", Color(0xFF2DD4BF))

            Spacer(modifier = Modifier.weight(1f))
            Text(
                "نسخة تأسيسية للواجهة — الصوت والحسابات والخدمات الخلفية لم تُربط بعد",
                color = Muted,
                fontSize = 11.sp
            )
        }
    }
}

@Composable
private fun RoomCard(title: String, subtitle: String, status: String, accent: Color) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White.copy(alpha = 0.06f), RoundedCornerShape(22.dp))
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Box(
            modifier = Modifier
                .background(
                    Brush.linearGradient(listOf(accent.copy(alpha = 0.95f), Violet.copy(alpha = 0.55f))),
                    RoundedCornerShape(16.dp)
                )
                .padding(18.dp)
        ) {
            Text("♫", color = Color.White, fontSize = 25.sp, fontWeight = FontWeight.Bold)
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 17.sp)
            Spacer(modifier = Modifier.height(4.dp))
            Text(subtitle, color = Muted, fontSize = 13.sp)
            Spacer(modifier = Modifier.height(7.dp))
            Text(status, color = accent, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        }
    }
}
