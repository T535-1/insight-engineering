# core/explain/attribution.py
from __future__ import annotations
from typing import Dict, List, Tuple, Optional
from math import isfinite

BASELINE_DEFAULT = 70.0

def _safe_float(x) -> float:
    try:
        v = float(x)
        return v if isfinite(v) else 0.0
    except Exception:
        return 0.0

def relative_contributions(
    scores: Dict[str, float],
    *,
    baseline: float = BASELINE_DEFAULT,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    يحسب مساهمة نسبية موقعة لكل بُعد حول خط الأساس.
    - يضرب الفارق بالوزن إن وُجد.
    - يطبع النتيجة كنسبة مئوية مجموع مطلقاتها ≈ 100 (إن أمكن).
    """
    diffs = {k: _safe_float(scores.get(k, 0.0)) - baseline for k in scores}
    weighted = {k: v * _safe_float((weights or {}).get(k, 1.0)) for k, v in diffs.items()}

    total_abs = sum(abs(v) for v in weighted.values()) or 1.0
    contrib_pct = {k: (v / total_abs) * 100.0 for k, v in weighted.items()}
    return contrib_pct  # موجب = داعم، سالب = حدّي

def top_factors(
    contributions: Dict[str, float], k: int = 3
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """
    يرجع أعلى k عوامل داعمة (إشارة موجبة) وأعلى k عوامل حدّية (سالبة).
    """
    positives = sorted([(k, v) for k, v in contributions.items() if v > 0], key=lambda x: x[1], reverse=True)
    negatives = sorted([(k, v) for k, v in contributions.items() if v < 0], key=lambda x: x[1])  # الأكثر سلبًا أولًا
    return positives[:k], negatives[:k]

def explain_summary(
    scores: Dict[str, float],
    *,
    baseline: float = BASELINE_DEFAULT,
    weights: Optional[Dict[str, float]] = None,
    top_k: int = 3
) -> Dict[str, object]:
    """
    ملخص تفسير: مساهمات نسبية، أعلى داعمة وحدّية، وخلاصة نصية قصيرة.
    """
    contrib = relative_contributions(scores, baseline=baseline, weights=weights)
    top_pos, top_neg = top_factors(contrib, k=top_k)

    def _fmt(items: List[Tuple[str, float]]) -> List[str]:
        return [f"{name}: {value:+.1f}%" for name, value in items]

    summary_text = "Top supporting → " + ", ".join(_fmt(top_pos)) + " | Top limiting → " + ", ".join(_fmt(top_neg))
    return {
        "baseline": baseline,
        "contributions_pct": contrib,
        "top_supporting": top_pos,
        "top_limiting": top_neg,
        "summary": summary_text,
    }
