# core/scoring/indices.py
from __future__ import annotations
from typing import Dict, Optional, Tuple
from .aggregators import weighted_mean

def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

def normalize_scores(scores: Dict[str, float], lo: float = 0.0, hi: float = 100.0) -> Dict[str, float]:
    return {k: clamp(float(v), lo, hi) for k, v in scores.items()}

def balance_index(scores: Dict[str, float], weights: Optional[Dict[str, float]] = None) -> Tuple[float, Dict[str, float]]:
    """يرجع (المؤشر الكلي، الدرجات بعد التطبيع)."""
    s_norm = normalize_scores(scores)
    idx = weighted_mean(s_norm, weights)
    return (round(idx, 2), s_norm)
