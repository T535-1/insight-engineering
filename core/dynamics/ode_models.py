# core/dynamics/ode_models.py
from __future__ import annotations
import numpy as np
from typing import Tuple, Callable

def simple_emotion_model(a=0.8, b=0.9, c=0.2, d=0.6, e=1.0) -> Callable:
    """
    نموذج مبسط لحركية حالتين (x=هدوء/توتر, y=وضوح/ارتباك).
    dx/dt = a*x - b*y - c*x^3
    dy/dt = d*x - e*y
    """
    def f(t: float, state: Tuple[float, float]):
        x, y = state
        dx = a * x - b * y - c * (x**3)
        dy = d * x - e * y
        return np.array([dx, dy])
    return f
