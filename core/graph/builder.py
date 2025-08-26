# core/graph/builder.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Tuple, Any
import networkx as nx
from core.utils.io import read_yaml

ROOT = Path(__file__).resolve().parents[2]

def load_graph_config() -> Dict[str, Any]:
    cfg_path = ROOT / "configs" / "graph.yaml"
    return read_yaml(cfg_path)

def build_graph(cfg: Dict[str, Any]) -> nx.Graph:
    nodes = cfg.get("nodes", [])
    edges = cfg.get("edges", [])
    G = nx.Graph()
    for n in nodes:
        G.add_node(n)
    for e in edges:
        if len(e) == 3:
            u, v, w = e
        elif len(e) == 2:
            u, v = e
            w = 1.0
        else:
            continue
        G.add_edge(u, v, weight=float(w))
    return G

def graph_from_config() -> nx.Graph:
    cfg = load_graph_config()
    return build_graph(cfg)
