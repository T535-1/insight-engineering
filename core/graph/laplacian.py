# core/graph/laplacian.py
from __future__ import annotations
from typing import Dict
import networkx as nx

def laplacian_smoothing(
    G: nx.Graph,
    scores: Dict[str, float],
    p: float = 2.0,
    alpha: float = 0.5,
    iterations: int = 5
) -> Dict[str, float]:
    """
    يقوم بتنعيم الدرجات على الشبكة:
    - p=2.0 يعطي المتوسط العادي (Laplacian).
    - p!=2 يعطي تأثير غير خطي (p-Laplacian).
    - alpha يتحكم في قوة التحديث.
    """
    x = scores.copy()
    for _ in range(iterations):
        new_x = x.copy()
        for node in G.nodes():
            neigh = list(G.neighbors(node))
            if not neigh:
                continue
            diff_sum = 0.0
            for nb in neigh:
                w = G[node][nb].get("weight", 1.0)
                diff = x[nb] - x[node]
                diff_sum += w * (abs(diff) ** (p - 2)) * diff if p != 2 else w * diff
            new_x[node] = x[node] + alpha * diff_sum / len(neigh)
        x = new_x
    return x
