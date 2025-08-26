# core/questionnaire.py
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from .utils.io import read_yaml

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_FACETS = ["Mind", "Heart", "Body", "Spirit", "Relations", "Work"]
DEFAULT_SCORE = 70

def load_questionnaire() -> Dict[str, Any]:
    p = ROOT / "configs" / "questionnaire.yaml"
    cfg = read_yaml(p)
    facets = cfg.get("facets") or DEFAULT_FACETS
    default_score = cfg.get("default_score", DEFAULT_SCORE)
    return {"facets": facets, "default_score": default_score}

def default_scores(facets: List[str], fill: int) -> Dict[str, float]:
    return {f: float(fill) for f in facets}
