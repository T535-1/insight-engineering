# core/config.py
from __future__ import annotations
from pathlib import Path
import os
from typing import Any, Dict, Optional
import yaml

ROOT = Path(__file__).resolve().parents[1]

def _read_yaml(p: Path) -> Dict[str, Any]:
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

class AppConfig:
    def __init__(self, cfg: Optional[Dict[str, Any]] = None):
        cfg = cfg or {}
        self.title_ar: str = cfg.get("title_ar", "هندسة البصيرة")
        self.title_en: str = cfg.get("title_en", "Insight Engineering")
        self.env: str = cfg.get("env", os.getenv("APP_ENV", "dev"))

def load_config() -> AppConfig:
    yaml_cfg = _read_yaml(ROOT / "configs" / "app.yaml")
    return AppConfig(yaml_cfg)
