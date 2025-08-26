from __future__ import annotations
from typing import Dict, List
import re
import numpy as np

# ============================================================
# 🔹 قوائم مبدئية للكلمات المفتاحية الإيجابية والسلبية
# ============================================================
POSITIVE_WORDS = [
    "happy", "calm", "grateful", "excited", "motivated", "peace",
    "joy", "love", "confident", "relaxed", "success"
]
NEGATIVE_WORDS = [
    "stressed", "sad", "angry", "tired", "worried", "confused",
    "upset", "failure", "depressed", "fear", "anxious"
]

# ============================================================
# 🔹 تنظيف النصوص من الرموز والمسافات الزائدة
# ============================================================
def clean_text(text: str) -> str:
    """تنظيف النص من الرموز غير المهمة وتحويله لأحرف صغيرة."""
    return re.sub(r"[^a-zA-Z\s]", "", text).strip().lower()

# ============================================================
# 🔹 حساب درجة الشعور العاطفي الأساسي (Sentiment Score)
# ============================================================
def sentiment_score(text: str) -> float:
    """
    حساب درجة الشعور: موجب = إيجابي، سالب = سلبي.
    النطاق: [-1, +1]
    """
    txt = clean_text(text)
    words = txt.split()
    if not words:
        return 0.0

    pos = sum(w in POSITIVE_WORDS for w in words)
    neg = sum(w in NEGATIVE_WORDS for w in words)
    score = (pos - neg) / max(1, len(words))
    return round(score, 3)

# ============================================================
# 🔹 دالة متوافقة مع rules.py
# ============================================================
def analyze_text_sentiment(text: str) -> Dict[str, float]:
    """
    تحليل النصوص لتوليد مؤشرات الشعور:
    - sentiment_score: بين -1 و +1
    - sentiment_label: إيجابي / سلبي / محايد
    """
    score = sentiment_score(text)
    if score > 0.1:
        label = "positive"
    elif score < -0.1:
        label = "negative"
    else:
        label = "neutral"
    return {"sentiment_score": score, "sentiment_label": label}

# ============================================================
# 🔹 استخراج الكلمات المفتاحية (Keyword Extraction)
# ============================================================
def keyword_extraction(text: str, top_k: int = 5) -> List[str]:
    """
    استخراج الكلمات الأكثر تكرارًا (يمكن تطويرها لاحقًا باستخدام TF-IDF أو BERT).
    """
    txt = clean_text(text)
    words = [w for w in txt.split() if len(w) > 3]
    if not words:
        return []

    freqs = {}
    for w in words:
        freqs[w] = freqs.get(w, 0) + 1

    sorted_words = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:top_k]]

# ============================================================
# 🔹 التحليل الكامل للنصوص
# ============================================================
def analyze_text(text: str) -> Dict[str, object]:
    """
    تحليل كامل للنصوص:
    - حساب الشعور (score + label)
    - استخراج الكلمات المفتاحية
    - حساب طول النص
    """
    sentiment_data = analyze_text_sentiment(text)
    return {
        "sentiment_score": sentiment_data["sentiment_score"],
        "sentiment_label": sentiment_data["sentiment_label"],
        "keywords": keyword_extraction(text),
        "length": len(text.split())
    }
