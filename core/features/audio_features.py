from __future__ import annotations
from typing import Dict, Any, Union
import numpy as np
import librosa
import tempfile
import os

# ============================================================
# 📌 تحميل الملف الصوتي
# ============================================================
def load_audio(file_path: str, sr: int = 16000):
    """تحميل الملف الصوتي وتحويله إلى Mono مع معدل عينات ثابت."""
    signal, sr = librosa.load(file_path, sr=sr, mono=True)
    return signal, sr

# ============================================================
# 🔹 استخراج ميزات الصوت الأساسية
# ============================================================
def extract_energy(signal: np.ndarray) -> float:
    """حساب الطاقة الكلية للصوت (RMS Energy)."""
    return float(np.sqrt(np.mean(signal ** 2)))

def extract_pitch(signal: np.ndarray, sr: int) -> float:
    """تقدير طبقة الصوت (Pitch) باستخدام Autocorrelation."""
    pitches, magnitudes = librosa.piptrack(y=signal, sr=sr)
    pitch_values = pitches[magnitudes > np.median(magnitudes)]
    return float(np.median(pitch_values)) if len(pitch_values) > 0 else 0.0

def extract_speech_rate(signal: np.ndarray, sr: int) -> float:
    """تقدير معدل الكلام باستخدام Zero Crossing Rate."""
    zcr = librosa.feature.zero_crossing_rate(signal)
    avg_zcr = float(np.mean(zcr))
    return avg_zcr * sr / 1000.0  # مقاطع/ثانية

# ============================================================
# 🔹 حساب مؤشر التوتر العام
# ============================================================
def compute_stress_index(energy: float, pitch: float, speech_rate: float) -> float:
    """
    مؤشر التوتر: قياس مبدئي يجمع بين الطاقة + طبقة الصوت + معدل الكلام.
    نطاق القيم ~ [0, 100].
    """
    stress = (energy * 50) + (pitch / 300.0 * 30) + (speech_rate * 20)
    return round(min(100, stress), 2)

# ============================================================
# 🔹 الدالة الرئيسية لتحليل الصوت (مستخدمة في Insight Engineering)
# ============================================================
def analyze_audio(file_obj: Union[str, bytes]) -> Dict[str, Any]:
    """
    تحليل الملف الصوتي واستخراج المؤشرات الأساسية:
    - المدة الزمنية
    - متوسط مستوى الطاقة
    - النغمة الأساسية (Pitch)
    - طاقة الطيف Spectral Energy
    """
    try:
        # التعامل مع BytesIO من Streamlit
        if not isinstance(file_obj, str):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(file_obj.read())
                tmp_path = tmp.name
            file_path = tmp_path
        else:
            file_path = file_obj

        # تحميل الملف الصوتي
        y, sr = librosa.load(file_path, sr=None)

        # طول الملف بالثواني
        duration = librosa.get_duration(y=y, sr=sr)

        # متوسط مستوى الطاقة (Root Mean Square Energy)
        rms = np.mean(librosa.feature.rms(y=y))

        # الطيف الطاقي
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

        # تقدير النغمة الأساسية (Pitch)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = np.mean(pitches[magnitudes > np.median(magnitudes)]) if np.any(magnitudes) else 0

        # تقدير نسبة الصمت
        silence_ratio = np.mean(y == 0) if len(y) > 0 else 0

        # تحليل المشاعر
        emotion_analysis = analyze_audio_emotions(file_path)

        # تنظيف الملفات المؤقتة
        if not isinstance(file_obj, str):
            os.remove(file_path)

        # مؤشرات جاهزة للإرجاع
        return {
            "duration_sec": round(duration, 2),
            "rms_energy": round(float(rms), 4),
            "spectral_centroid": round(float(spectral_centroid), 2),
            "pitch_hz": round(float(pitch), 2),
            "silence_ratio": round(float(silence_ratio), 3),
            "emotion_analysis": emotion_analysis
        }

    except Exception as e:
        return {
            "error": str(e),
            "duration_sec": None,
            "rms_energy": None,
            "spectral_centroid": None,
            "pitch_hz": None,
            "silence_ratio": None,
            "emotion_analysis": None
        }

# ============================================================
# 🔹 التحليل العاطفي للصوت (اختياري)
# ============================================================
def analyze_audio_emotions(file_path: str) -> Dict[str, Any]:
    """
    تحليل المشاعر بناءً على ميزات الصوت:
    - الطاقة
    - طبقة الصوت
    - معدل الكلام
    - مؤشر التوتر
    - التصنيف النهائي: إيجابي / محايد / سلبي
    """
    try:
        signal, sr = load_audio(file_path)
        energy = extract_energy(signal)
        pitch = extract_pitch(signal, sr)
        speech_rate = extract_speech_rate(signal, sr)
        stress_idx = compute_stress_index(energy, pitch, speech_rate)

        if stress_idx < 35:
            sentiment = "positive"
        elif stress_idx < 65:
            sentiment = "neutral"
        else:
            sentiment = "negative"

        return {
            "energy": round(energy, 3),
            "pitch": round(pitch, 2),
            "speech_rate": round(speech_rate, 2),
            "stress_index": stress_idx,
            "sentiment": sentiment
        }

    except Exception as e:
        return {"error": str(e)}
