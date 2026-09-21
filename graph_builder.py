"""
Knowledge Graph Builder & Entity Extraction Module.
Extracts domain entities via rule-based matching and builds semantic NetworkX graphs,
visualized via interactive Plotly figures.
"""

import re
from typing import List, Dict, Tuple, Any, Set
import networkx as nx
import plotly.graph_objects as go


# Standard Rule-Based Entity Vocabulary
ENTITY_VOCABULARY = [
    "Artificial Intelligence",
    "AI",
    "Machine Learning",
    "Deep Learning",
    "Neural Network",
    "Cybersecurity",
    "Malware",
    "Bias",
    "Ethics",
    "Governance",
    "Healthcare",
    "Privacy",
    "Detection",
    "Automation",
    "Robotics",
    "Data",
    "Algorithm",
    "Knowledge Graph",
    "Information Retrieval",
    "TF-IDF",
    "Cosine Similarity",
    "Documents"
]

# Predefined Knowledge Graph Semantic Tuples (Source, Relation, Target)
PREDEFINED_RELATIONSHIPS: List[Tuple[str, str, str]] = [
    ("Artificial Intelligence", "uses", "Machine Learning"),
    ("Machine Learning", "includes", "Deep Learning"),
    ("Deep Learning", "uses", "Neural Network"),
    ("Cybersecurity", "detects", "Malware"),
    ("Ethics", "addresses", "Bias"),
    ("Governance", "regulates", "Artificial Intelligence"),
    ("Healthcare", "uses", "Artificial Intelligence"),
    ("Privacy", "protects", "Data"),
    ("Automation", "uses", "Algorithm"),
    ("Knowledge Graph", "enhances", "Information Retrieval"),
    ("TF-IDF", "retrieves", "Documents"),
    ("Cosine Similarity", "ranks", "Documents")
]

# Category and Color Scheme
NODE_CATEGORIES: Dict[str, str] = {
    # AI - Blue
    "Artificial Intelligence": "AI",
    "AI": "AI",
    "Machine Learning": "AI",
    "Deep Learning": "AI",
    "Neural Network": "AI",
    "Robotics": "AI",
    # Domain - Green
    "Healthcare": "Domain",
    "Governance": "Domain",
    "Documents": "Domain",
    # Technology - Orange
    "Knowledge Graph": "Technology",
    "Information Retrieval": "Technology",
    "TF-IDF": "Technology",
    "Cosine Similarity": "Technology",
    "Algorithm": "Technology",
    "Data": "Technology",
    "Automation": "Technology",
    # Ethics - Purple
    "Ethics": "Ethics",
    "Bias": "Ethics",
    "Privacy": "Ethics",
    # Threat - Red
    "Cybersecurity": "Threat",
    "Malware": "Threat",
    "Detection": "Threat"
}

CATEGORY_HEX_COLORS: Dict[str, str] = {
    "AI": "#2563EB",         # Blue
    "Domain": "#16A34A",     # Green
    "Technology": "#EA580C", # Orange
    "Ethics": "#9333EA",     # Purple
    "Threat": "#DC2626"      # Red
}


def extract_entities(text: str) -> Dict[str, int]:
    """
    Performs case-insensitive, rule-based entity extraction.
    Removes duplicates and counts frequencies of recognized concepts.
    
    Args:
        text: Combined text from retrieved documents.
        
    Returns:
        Dict mapping entity name to occurrence count, sorted descending.
    """
    if not text:
        return {}

    entity_counts: Dict[str, int] = {}

    for entity in ENTITY_VOCABULARY:
        # Avoid matching standalone single characters or parts of larger words
        # For acronyms like AI or TF-IDF, use strict word boundaries
        escaped = re.escape(entity)
        pattern = rf"\b{escaped}\b"
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        count = len(matches)
        if count > 0:
            entity_counts[entity] = count

    # Sort entities by frequency descending
    sorted_entities = dict(sorted(entity_counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_entities


def build_knowledge_graph(extracted_entities: Dict[str, int]) -> Tuple[nx.DiGraph, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Builds a NetworkX directed graph filtered by entities present in retrieved documents.
    
    Args:
        extracted_entities: Dictionary of extracted entity strings and counts.
        
    Returns:
        Tuple of (NetworkX DiGraph, list of node dicts, list of edge dicts)
    """
    G = nx.DiGraph()
    present_keys: Set[str] = set(extracted_entities.keys())

    # Build edges if both entities exist in the retrieved entities,
    # or if an entity connects to "Documents" which represents corpus targets
    active_edges: List[Dict[str, Any]] = []
    active_nodes_set: Set[str] = set()

    for source, relation, target in PREDEFINED_RELATIONSHIPS:
        # Condition: Include relationship if both entities or source + target are in the extracted set
        # 'Documents' is automatically included if TF-IDF or Cosine Similarity was extracted
        source_present = source in present_keys
        target_present = target in present_keys or (target == "Documents" and source_present)

        if source_present and target_present:
            G.add_edge(source, target, relation=relation)
            active_nodes_set.add(source)
            active_nodes_set.add(target)
            active_edges.append({
                "source": source,
                "relation": relation,
                "target": target
            })

    # If no predefined edges match, add isolated nodes for prominent extracted entities
    # so the student still sees the extracted conceptual graph
    if len(active_edges) == 0:
        for ent in list(present_keys)[:8]:
            G.add_node(ent)
            active_nodes_set.add(ent)
    else:
        # Also ensure all top extracted entities are added as nodes
        for ent in list(present_keys)[:10]:
            if ent not in G:
                G.add_node(ent)
                active_nodes_set.add(ent)

    # Format nodes list
    node_data_list = []
    for node in G.nodes():
        category = NODE_CATEGORIES.get(node, "Technology")
        color = CATEGORY_HEX_COLORS.get(category, "#2563EB")
        freq = extracted_entities.get(node, 1)
        node_data_list.append({
            "name": node,
            "category": category,
            "color": color,
            "frequency": freq
        })

    return G, node_data_list, active_edges


def render_graph_plotly(G: nx.DiGraph, extracted_entities: Dict[str, int]) -> go.Figure:
    """
    Generates an interactive Plotly visualization for the knowledge graph.
    Includes spring layout, edge labels, hover metadata, and category color coding.
    """
    if len(G.nodes()) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No matching entities found in retrieved documents.",
            showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(
            height=450,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig

    # Compute node positions using spring layout
    pos = nx.spring_layout(G, seed=42, k=1.4, iterations=50)

    # Prepare Edge Traces (Lines)
    edge_x = []
    edge_y = []
    edge_mid_x = []
    edge_mid_y = []
    edge_mid_text = []

    for edge in G.edges(data=True):
        u, v, data = edge
        x0, y0 = pos[u]
        x1, y1 = pos[v]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

        # Midpoint for edge relation label
        mid_x = (x0 + x1) / 2.0
        mid_y = (y0 + y1) / 2.0
        edge_mid_x.append(mid_x)
        edge_mid_y.append(mid_y)
        edge_mid_text.append(data.get("relation", "relates"))

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1.8, color="#94A3B8"),
        hoverinfo="none",
        mode="lines"
    )

    edge_label_trace = go.Scatter(
        x=edge_mid_x,
        y=edge_mid_y,
        mode="text",
        text=edge_mid_text,
        textposition="middle center",
        textfont=dict(size=11, color="#475569"),
        hoverinfo="none"
    )

    # Prepare Node Traces
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes = []
    hover_texts = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

        category = NODE_CATEGORIES.get(node, "Technology")
        color = CATEGORY_HEX_COLORS.get(category, "#2563EB")
        freq = extracted_entities.get(node, 1)

        node_colors.append(color)
        # Scaled node size based on frequency
        size = min(36, max(18, 16 + freq * 2))
        node_sizes.append(size)

        in_deg = G.in_degree(node) if hasattr(G, "in_degree") else 0
        out_deg = G.out_degree(node) if hasattr(G, "out_degree") else 0
        hover_texts.append(
            f"<b>{node}</b><br>"
            f"Category: {category}<br>"
            f"Occurrences: {freq}<br>"
            f"Connections: {in_deg + out_deg}"
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        textfont=dict(size=12, family="sans-serif", color="#0F172A"),
        hoverinfo="text",
        hovertext=hover_texts,
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color="#FFFFFF")
        )
    )

    # Build Layout
    fig = go.Figure(data=[edge_trace, edge_label_trace, node_trace])
    fig.update_layout(
        title=dict(
            text="Knowledge Graph: Retrieved Entities & Semantic Relations",
            font=dict(size=15)
        ),
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=20, r=20, t=50),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=520
    )

    return fig
