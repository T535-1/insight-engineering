from __future__ import annotations
from typing import Dict, Any, Optional
import numpy as np

# ============================================================
# 🔹 دالة لتطبيع القيم بين 0 و 1
# ============================================================
def normalize(value: float, vmin: float, vmax: float) -> float:
    try:
        return max(0.0, min(1.0, (value - vmin) / (vmax - vmin)))
    except ZeroDivisionError:
        return 0.0

# ============================================================
# 🔹 حساب مؤشرات الصحة الحيوية
# ============================================================
def compute_health_indices(
    hr: Optional[float] = None,
    hrv: Optional[float] = None,
    sleep_score: Optional[float] = None,
    activity_score: Optional[float] = None,
    stress_score: Optional[float] = None
) -> Dict[str, Any]:
    """
    حساب مؤشرات الصحة العامة اعتمادًا على بيانات القياسات الحيوية:
    - معدل ضربات القلب (hr) بالنبضة/دقيقة (BPM)
    - تباين معدل ضربات القلب (hrv) بالملي ثانية
    - sleep_score: جودة النوم (0-100)
    - activity_score: النشاط البدني (0-100)
    - stress_score: مستوى التوتر من الجهاز (0-100)
    """
    results: Dict[str, Any] = {}

    # -------------------------------------
    # 🫀 معدل ضربات القلب (Heart Rate)
    # -------------------------------------
    if hr is not None and hr > 0:
        # نطاق صحي للبالغين: 60-100 bpm
        hr_norm = 1 - normalize(hr, 60, 100)
        results["heart_rate"] = round(hr, 1)
        results["heart_health_index"] = round(hr_norm * 100, 2)
    else:
        results["heart_rate"] = None
        results["heart_health_index"] = None

    # -------------------------------------
    # 💓 تباين معدل ضربات القلب (HRV)
    # -------------------------------------
    if hrv is not None and hrv > 0:
        # قيمة مثالية: 60ms+
        hrv_norm = normalize(hrv, 20, 80)
        results["hrv"] = round(hrv, 1)
        results["relaxation_index"] = round(hrv_norm * 100, 2)
    else:
        results["hrv"] = None
        results["relaxation_index"] = None

    # -------------------------------------
    # 🛌 جودة النوم (Sleep Score)
    # -------------------------------------
    results["sleep_score"] = round(sleep_score, 1) if sleep_score is not None else None

    # -------------------------------------
    # 🏃 النشاط البدني (Activity Score)
    # -------------------------------------
    results["activity_score"] = round(activity_score, 1) if activity_score is not None else None

    # -------------------------------------
    # 😮‍💨 مستوى التوتر من الجهاز (Stress Score)
    # -------------------------------------
    results["device_stress_score"] = round(stress_score, 1) if stress_score is not None else None

    # -------------------------------------
    # 🧠 حساب مؤشر الصحة العام (Overall Health Index)
    # -------------------------------------
    components = []
    for key in ["heart_health_index", "relaxation_index", "sleep_score", "activity_score"]:
        val = results.get(key)
        if isinstance(val, (int, float)):
            components.append(val)

    results["overall_health_index"] = round(np.mean(components), 2) if components else None

    return results

# ============================================================
# 🔹 تحليل البيانات القادمة من الأجهزة أو API
# ============================================================
def analyze_wearable_signals(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    تحليل البيانات القادمة من أجهزة القياس Wearable أو API خارجي.
    البيانات المتوقعة:
    {
      "hr": 72,
      "hrv": 55,
      "sleep_score": 85,
      "activity_score": 60,
      "stress_score": 25
    }
    """
    try:
        return compute_health_indices(
            hr=data.get("hr"),
            hrv=data.get("hrv"),
            sleep_score=data.get("sleep_score"),
            activity_score=data.get("activity_score"),
            stress_score=data.get("stress_score"),
        )
    except Exception as e:
        return {"error": f"Signal analysis failed: {str(e)}"}
