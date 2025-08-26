# core/utils/validators.py
from __future__ import annotations
from typing import Iterable, List

def is_number(x) -> bool:
    try:
        float(x)
        return True
    except Exception:
        return False

def validate_scores(scores: Iterable) -> List[float]:
    vals = [float(s) for s in scores if is_number(s)]
    if not vals:
        raise ValueError("Scores list is empty or invalid.")
    return vals
