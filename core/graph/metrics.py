# core/graph/metrics.py
from __future__ import annotations
from typing import Dict
import networkx as nx

def degree_centrality(G: nx.Graph) -> Dict[str, float]:
    return nx.degree_centrality(G)

def weighted_degree(G: nx.Graph) -> Dict[str, float]:
    return {n: sum(d.get("weight", 1.0) for _, _, d in G.edges(n, data=True)) for n in G.nodes()}
