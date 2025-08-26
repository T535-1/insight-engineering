# core/scoring/aggregators.py
from __future__ import annotations
from typing import Dict, Optional

def weighted_mean(scores: Dict[str, float], weights: Optional[Dict[str, float]] = None) -> float:
    if not scores:
        return 0.0
    if not weights:
        return sum(scores.values()) / len(scores)
    num, den = 0.0, 0.0
    for k, v in scores.items():
        w = float(weights.get(k, 1.0))
        num += v * w
        den += w
    return num / den if den else 0.0
