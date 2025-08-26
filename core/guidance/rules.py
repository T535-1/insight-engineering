# ============================================================
# 📌 هندسة البصيرة Insight Engineering
# ملف: core/guidance/rules.py
# الوظائف:
#   - تحميل ودمج قواعد الإرشاد الافتراضية من configs/guidance.yaml
#   - اختيار الأبعاد الأضعف حسب نتائج التقييم
#   - تحليل النص والصوت والإشارات الحيوية
#   - توليد توصيات شخصية ديناميكية
# ============================================================

from __future__ import annotations
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field

# 🛠️ استدعاء أدوات التحليل
from core.utils.io import read_yaml
from core.features.text_features import analyze_text_sentiment
from core.features.audio_features import analyze_audio_emotions
from core.features.signal_features import analyze_wearable_signals

ROOT = Path(__file__).resolve().parents[2]

# ============================================================
# 🔹 القواعد الافتراضية الأساسية
# ============================================================

DEFAULT_RULES: Dict[str, List[str]] = {
    "Mind": [
        "تنفّس واعٍ 5 دقائق + كتابة 3 أسطر عن فكرة تقلقك.",
        "إيقاف مُشتتات 20 دقيقة (هاتف/إشعارات) ثم تركيز عميق."
    ],
    "Heart": [
        "تواصل رحيم: أرسل رسالة تقدير لشخص قريب.",
        "تمرين امتنان: اكتب شيئين ممتنًا لهما اليوم."
    ],
    "Body": [
        "مشي خفيف 10–15 دقيقة أو تمدّد بسيط.",
        "شرب ماء كافٍ وتقليل السكر اليوم."
    ],
    "Spirit": [
        "ذكر/تأمل قصير 7 دقائق مع نية واضحة.",
        "قراءة فقرة مُلهِمة وتطبيق معنى واحد عمليًا."
    ],
    "Relations": [
        "مكالمة قصيرة لشخص لك عنده واجب عاطفي.",
        "استماع نشط دون مقاطعة لمدة 5 دقائق."
    ],
    "Work": [
        "اختَر مهمة واحدة فقط وأنهِها تمامًا (Pomodoro 25).",
        "لائحة 3 أولويات واقعية لهذا اليوم."
    ],
}

@dataclass
class Recommendation:
    facet: str
    priority: float
    tips: List[str] = field(default_factory=list)

# ============================================================
# 🔹 تحميل ودمج القواعد
# ============================================================

def load_guidance_config() -> Dict[str, List[str]]:
    """
    يقرأ configs/guidance.yaml ويعيد قاموسًا مرتبًا: {facet: [tips]}
    """
    cfg = read_yaml(ROOT / "configs" / "guidance.yaml")
    rules = cfg.get("rules", []) or []
    by_facet: Dict[str, List[str]] = {}
    for item in rules:
        f = str(item.get("facet", "")).strip()
        tip = str(item.get("tip", "")).strip()
        if f and tip:
            by_facet.setdefault(f, []).append(tip)
    return by_facet


def merge_rules() -> Dict[str, List[str]]:
    """
    يدمج القواعد الافتراضية مع القواعد المضافة من configs/guidance.yaml
    """
    file_rules = load_guidance_config()
    merged = DEFAULT_RULES.copy()
    for facet, tips in file_rules.items():
        merged.setdefault(facet, [])
        for t in tips:
            if t not in merged[facet]:
                merged[facet].append(t)
    return merged

# ============================================================
# 🔹 تحديد الأبعاد الأضعف حسب الدرجات
# ============================================================

def weakest_facets(
    scores: Dict[str, float],
    *,
    k: int = 3,
    centrality: Optional[Dict[str, float]] = None,
    centrality_boost: float = 0.2
) -> List[Tuple[str, float]]:
    """
    يحدد أضعف k أبعاد مع مراعاة المركزية إذا توفرت.
    """
    if not scores:
        return []

    c = centrality or {}
    if c:
        c_vals = list(c.values())
        c_min, c_max = (min(c_vals), max(c_vals)) if c_vals else (0.0, 1.0)

        def c_norm(name: str) -> float:
            return 0.0 if c_max == c_min else (c.get(name, 0.0) - c_min) / (c_max - c_min)
    else:
        def c_norm(name: str) -> float:
            return 0.0

    priorities = []
    for facet, sc in scores.items():
        base_need = max(0.0, 100.0 - float(sc))
        boost = 1.0 + centrality_boost * c_norm(facet)
        priorities.append((facet, base_need * boost))

    priorities.sort(key=lambda x: x[1], reverse=True)
    return priorities[:k]


def recommend_for_scores(
    scores: Dict[str, float],
    *,
    k: int = 3,
    rules: Optional[Dict[str, List[str]]] = None,
    centrality: Optional[Dict[str, float]] = None
) -> List[Recommendation]:
    """
    يولّد توصيات لأضعف k أبعاد بناءً على الدرجات الحالية.
    """
    rules = rules or merge_rules()
    weak = weakest_facets(scores, k=k, centrality=centrality)

    recs: List[Recommendation] = []
    for facet, pr in weak:
        tips = rules.get(facet, []) or ["Tip: Apply a short focused practice in this facet."]
        recs.append(Recommendation(facet=facet, priority=round(pr, 2), tips=tips[:3]))
    return recs

# ============================================================
# 🔹 التحليل العاطفي ودمج البيانات
# ============================================================

def evaluate_emotional_state(text: str = None, audio_path: str = None) -> Dict[str, Any]:
    """
    تحليل النصوص والصوت لاستخراج المشاعر والمزاج.
    """
    results = {}
    if text:
        results["text_analysis"] = analyze_text_sentiment(text)
    if audio_path:
        results["audio_analysis"] = analyze_audio_emotions(audio_path)
    return results


def build_guidance_recommendations(
    text: str = None,
    audio_path: str = None,
    signals: Dict[str, Any] = None,
    lang: str = "en"
) -> Dict[str, Any]:
    """
    توليد توصيات مخصصة بناءً على:
    - تحليل النصوص
    - تحليل الصوت
    - تحليل بيانات الأجهزة القابلة للارتداء
    """
    emotional_data = evaluate_emotional_state(text=text, audio_path=audio_path)
    wearable_analysis = analyze_wearable_signals(signals or {})

    recommendations: List[str] = []
    mood = None

    # 🧠 تحليل مشاعر النصوص
    if emotional_data.get("text_analysis"):
        text_sentiment = emotional_data["text_analysis"].get("sentiment", "neutral")
        if text_sentiment == "positive":
            recommendations.append("🌟 Great! Keep maintaining your positive energy.")
            mood = "positive"
        elif text_sentiment == "neutral":
            recommendations.append("🙂 Stay balanced and mindful throughout the day.")
            mood = "neutral"
        else:
            recommendations.append("💡 Seems you're stressed. Try practicing deep breathing.")
            mood = "negative"

    # ❤️ تقييم الصحة العامة
    overall_health = wearable_analysis.get("overall_health_index")
    if overall_health is not None:
        if overall_health >= 80:
            recommendations.append("✅ Your physical condition looks great! Keep up the healthy habits.")
        elif overall_health >= 60:
            recommendations.append("⚠️ You may need moderate improvements in activity or sleep.")
        else:
            recommendations.append("🚨 Your health indicators need attention. Prioritize rest and balanced nutrition.")

    # 🛌 جودة النوم
    sleep_score = wearable_analysis.get("sleep_score")
    if sleep_score is not None and sleep_score < 60:
        recommendations.append("🛌 Try to improve your sleep hygiene for better mood stability.")

    # 🏃‍♂️ النشاط البدني
    activity_score = wearable_analysis.get("activity_score")
    if activity_score is not None and activity_score < 50:
        recommendations.append("🏃‍♂️ Consider adding 20 minutes of walking to your daily routine.")

    # 🌐 دعم الترجمة
    if lang == "ar":
        recommendations = [translate_to_ar(rec) for rec in recommendations]

    return {
        "emotional_data": emotional_data,
        "wearable_analysis": wearable_analysis,
        "overall_recommendations": recommendations,
        "mood_estimation": mood
    }

# ============================================================
# 🔹 مترجم التوصيات للعربية
# ============================================================

def translate_to_ar(text: str) -> str:
    translations = {
        "🌟 Great! Keep maintaining your positive energy.": "🌟 أحسنت! استمر في الحفاظ على طاقتك الإيجابية.",
        "🙂 Stay balanced and mindful throughout the day.": "🙂 ابقَ متوازنًا ومتيقظًا طوال اليوم.",
        "💡 Seems you're stressed. Try practicing deep breathing.": "💡 يبدو أنك متوتر. جرب تمارين التنفس العميق.",
        "✅ Your physical condition looks great! Keep up the healthy habits.": "✅ صحتك الجسدية ممتازة! استمر على العادات الصحية.",
        "⚠️ You may need moderate improvements in activity or sleep.": "⚠️ قد تحتاج لتحسينات بسيطة في النشاط أو النوم.",
        "🚨 Your health indicators need attention. Prioritize rest and balanced nutrition.": "🚨 تحتاج مؤشرات صحتك للاهتمام. احرص على الراحة والتغذية السليمة.",
        "🛌 Try to improve your sleep hygiene for better mood stability.": "🛌 حاول تحسين جودة نومك لاستقرار حالتك المزاجية.",
        "🏃‍♂️ Consider adding 20 minutes of walking to your daily routine.": "🏃‍♂️ أضف 20 دقيقة من المشي إلى روتينك اليومي."
    }
    return translations.get(text, text)
