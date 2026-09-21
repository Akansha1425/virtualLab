"""
Simulation Module for Information Retrieval & Knowledge Graphs Virtual Lab.
Provides the interactive experiment sandbox:
- Top Controls (Query, Top-K, Threshold)
- Document Corpus Loading & Indexing
- TF-IDF & Cosine Similarity Retrieval
- Document Preview Expander
- Rule-based Entity Extraction with Colored Badges
- Interactive Knowledge Graph (NetworkX + Plotly)
- Analytics Dashboard (Metrics, Bar Chart, Pie Chart)
- Experimental Trial Logger & CSV Exporter
"""

import os
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import plotly.express as px
import streamlit as st

from document_loader import load_documents
from retriever import build_index, retrieve, get_results_dataframe
from graph_builder import (
    extract_entities,
    build_knowledge_graph,
    render_graph_plotly,
    NODE_CATEGORIES,
    CATEGORY_HEX_COLORS
)


def ensure_sample_documents(folder_path: str = "documents"):
    """
    Checks if documents directory exists and contains sample documents.
    If empty, populates a diverse offline sample corpus across multiple domains.
    """
    os.makedirs(folder_path, exist_ok=True)
    existing_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if len(existing_files) > 0:
        return

    sample_docs = {
        "doc01_ai_and_machine_learning.txt": (
            "Artificial Intelligence is a wide-ranging branch of computer science committed to building smart machines. "
            "Artificial Intelligence uses Machine Learning as one of its primary computational engines. "
            "Machine Learning includes Deep Learning techniques that analyze massive quantities of Data through complex Algorithm models. "
            "Through Automation and Robotics, intelligent systems optimize industrial operations."
        ),
        "doc02_deep_learning_neural_networks.txt": (
            "Deep Learning uses Neural Network architectures inspired by biological nervous systems. "
            "These models perform hierarchical pattern recognition on input Data. "
            "Modern Artificial Intelligence relies heavily on Deep Learning for natural language processing and computer vision."
        ),
        "doc03_healthcare_ai_diagnostics.txt": (
            "Healthcare uses Artificial Intelligence to improve diagnostic precision and patient prognosis. "
            "Machine Learning models analyze clinical Data and medical imaging to provide early cancer Detection. "
            "Medical researchers emphasize that Automation must adhere to strict clinical trial standards and patient safety protocols."
        ),
        "doc04_cybersecurity_and_malware.txt": (
            "Modern Cybersecurity systems deploy real-time Detection mechanisms to protect critical computing infrastructure. "
            "Cybersecurity detects Malware, ransomware, and unauthorized intrusions using heuristic and behavioral analysis. "
            "Maintaining organizational Privacy requires robust defensive posture and continuous threat intelligence."
        ),
        "doc05_ai_ethics_and_bias.txt": (
            "In contemporary Artificial Intelligence deployment, Ethics addresses Bias in automated scoring algorithms. "
            "Algorithmic Bias can disadvantage marginalized populations if training Data is unrepresentative. "
            "Therefore, Governance regulates Artificial Intelligence to ensure accountability, fairness, and transparency."
        ),
        "doc06_data_privacy_and_governance.txt": (
            "Privacy protects Data against unauthorized exploitation and corporate overreach. "
            "Institutional Governance frameworks establish legal compliance standards for information lifecycle handling. "
            "Data protection regulations empower users with agency over personal information."
        ),
        "doc07_information_retrieval_and_tfidf.txt": (
            "Information Retrieval systems organize and search unstructured text collections. "
            "TF-IDF retrieves Documents by evaluating term frequency and inverse document frequency weights. "
            "Cosine Similarity ranks Documents based on the angle between the query vector and document vectors in multi-dimensional space."
        ),
        "doc08_knowledge_graphs_in_search.html": (
            "<html><body>"
            "<h1>Knowledge Graphs in Semantic Search</h1>"
            "<p>A Knowledge Graph enhances Information Retrieval by mapping unstructured keywords into structured concept nodes and semantic edges.</p>"
            "<p>Integrating a Knowledge Graph with statistical document search provides contextual exploration and entity relationship discovery across Documents.</p>"
            "</body></html>"
        ),
        "doc09_automation_and_robotics.txt": (
            "Automation uses Algorithm optimization to operate machines with minimal human intervention. "
            "Robotics combines mechanical engineering with Artificial Intelligence to deploy autonomous agents in manufacturing, logistics, and surgery."
        ),
        "doc10_threat_detection_in_healthcare.txt": (
            "Hospitals increasingly face digital intrusions. Cybersecurity detects Malware targeting patient records and diagnostic devices. "
            "Protecting Healthcare infrastructure requires continuous Detection and rigorous Privacy standards for medical Data."
        )
    }

    for filename, content in sample_docs.items():
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


def render_entity_badges(extracted_entities: Dict[str, int]):
    """
    Renders extracted entities as visually distinct category-colored badges using native markdown.
    """
    if not extracted_entities:
        st.info("No domain vocabulary entities detected in retrieved documents.")
        return

    badge_html_parts = []
    for entity, count in extracted_entities.items():
        category = NODE_CATEGORIES.get(entity, "Technology")
        color = CATEGORY_HEX_COLORS.get(category, "#2563EB")
        badge = (
            f"<span style='display:inline-block; background-color:{color}; color:#FFFFFF; "
            f"padding:4px 10px; margin:3px 4px; border-radius:14px; font-size:12px; font-weight:500;'>"
            f"{entity} ({count})</span>"
        )
        badge_html_parts.append(badge)

    container_html = (
        f"<div style='background-color:rgba(128,128,128,0.08); padding:12px; border-radius:8px; border:1px solid rgba(128,128,128,0.2);'>"
        f"{''.join(badge_html_parts)}</div>"
    )
    st.markdown(container_html, unsafe_allow_html=True)


def clear_simulation_session():
    """Callback to safely reset simulation session state before widgets instantiate."""
    keys_to_remove = [
        "retrieved_docs",
        "selected_doc",
        "entities",
        "relationships",
        "latest_results",
        "graph_data",
        "latest_result",
        "latest_retrieval",
        "selected_document",
        "current_query"
    ]

    for k in keys_to_remove:
        st.session_state.pop(k, None)

    st.session_state["sim_query_input"] = ""
    st.toast("Experimental session cleared.")


def render_simulation():
    """Renders Section 2: Interactive IR and Knowledge Graph Simulation Sandbox."""
    st.header("Section 2: Interactive Simulation Sandbox")
    st.markdown(
        "Execute TF-IDF vector retrieval on the document repository, examine cosine similarity ranking, "
        "extract domain entities, and visualize the dynamic semantic knowledge graph."
    )

    # Ensure document directory is ready
    ensure_sample_documents("documents")

    # Load and index documents in session state
    if "corpus_docs" not in st.session_state or st.session_state.get("reload_corpus", False):
        docs = load_documents("documents")
        st.session_state["corpus_docs"] = docs
        vectorizer, tfidf_matrix = build_index(docs)
        st.session_state["vectorizer"] = vectorizer
        st.session_state["tfidf_matrix"] = tfidf_matrix
        st.session_state["reload_corpus"] = False

    corpus_docs = st.session_state.get("corpus_docs", [])
    vectorizer = st.session_state.get("vectorizer")
    tfidf_matrix = st.session_state.get("tfidf_matrix")

    # Top Controls Section
    st.subheader("Experimental Search & Retrieval Controls")
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2.5, 1, 1.5])

    if "sim_query_input" not in st.session_state:
        st.session_state["sim_query_input"] = ""

    with ctrl_col1:
        query_input = st.text_input(
            "Enter Search Query",
            key="sim_query_input",
            placeholder="e.g., types of AI, machine learning in healthcare, cybersecurity malware detection"
        )

    with ctrl_col2:
        top_k = st.selectbox(
            "Top-K Results:",
            options=[3, 4, 5, 6, 7, 8, 9, 10],
            index=2,
            key="sim_top_k"
        )

    with ctrl_col3:
        threshold = st.slider(
            "Cosine Similarity Threshold:",
            min_value=0.0,
            max_value=1.0,
            value=0.05,
            step=0.05,
            key="sim_threshold"
        )

    btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 4])
    with btn_col1:
        run_retrieve = st.button("Retrieve Documents", type="primary", use_container_width=True)
    with btn_col2:
        st.button(
            "Clear Session",
            on_click=clear_simulation_session,
            use_container_width=True
        )

    # 2. Validate Empty Query on button click
    if run_retrieve:
        clean_query = query_input.strip() if query_input else ""
        if not clean_query:
            st.warning("Please enter a search query before retrieving documents.")
        else:
            st.session_state["current_query"] = clean_query
            ranked_docs = retrieve(
                query=clean_query,
                top_k=top_k,
                threshold=threshold,
                documents=corpus_docs,
                vectorizer=vectorizer,
                tfidf_matrix=tfidf_matrix
            )
            combined_text = " ".join([d.get("text", "") for d in ranked_docs])
            extracted_entities = extract_entities(combined_text)
            G, node_data, active_edges = build_knowledge_graph(extracted_entities)
            avg_sim = (
                sum(d.get("similarity_score", d.get("similarity", 0.0)) for d in ranked_docs) / len(ranked_docs)
                if ranked_docs else 0.0
            )
            result_state = {
                "query": clean_query,
                "top_k": top_k,
                "threshold": threshold,
                "retrieved_docs": ranked_docs,
                "extracted_entities": extracted_entities,
                "entities": list(extracted_entities.keys()),
                "relationships": active_edges,
                "entity_frequency": extracted_entities,
                "graph": G,
                "node_data": node_data,
                "active_edges": active_edges,
                "average_similarity": avg_sim,
                "avg_similarity": avg_sim,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state["latest_result"] = result_state
            st.session_state["latest_retrieval"] = result_state

    # Defensive retrieval state access
    latest = st.session_state.get("latest_result")
    if latest is None:
        latest = st.session_state.get("latest_retrieval")

    if latest is None:
        latest = {
            "query": "",
            "retrieved_docs": [],
            "entities": [],
            "relationships": [],
            "entity_frequency": {},
            "extracted_entities": {},
            "active_edges": [],
            "node_data": [],
            "graph": None,
            "average_similarity": 0.0,
            "avg_similarity": 0.0,
            "top_k": top_k,
            "threshold": threshold,
            "timestamp": ""
        }
        st.session_state["latest_result"] = latest
        st.session_state["latest_retrieval"] = latest

    ranked_docs: List[Dict[str, Any]] = latest.get("retrieved_docs", [])
    extracted_entities: Dict[str, int] = latest.get("extracted_entities", latest.get("entity_frequency", {}))
    G = latest.get("graph")
    node_data = latest.get("node_data", [])
    active_edges = latest.get("active_edges", latest.get("relationships", []))
    has_retrieval = bool(latest.get("query"))

    st.divider()

    # Main Tabs: Retrieval & Preview, Knowledge Graph, Analytics, Trial Logger
    tab_results, tab_graph, tab_analytics, tab_logger = st.tabs([
        "1. Ranked Retrieval & Document Preview",
        "2. Knowledge Graph Visualization",
        "3. Analytics & Corpus Distribution",
        "4. Experimental Trial Recording"
    ])

    # Tab 1: Retrieval Table & Document Preview
    with tab_results:
        st.subheader("Retrieved Documents Ranking Table")
        if not has_retrieval:
            st.info("No retrieval has been performed yet. Enter a query and click Retrieve Documents.")
        elif ranked_docs:
            df_display = get_results_dataframe(ranked_docs)
            st.dataframe(df_display, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("Document Inspection & Content Preview")
            doc_options = [f"{d['rank']}. {d['filename']} ({d['similarity_pct']})" for d in ranked_docs]
            selected_option = st.selectbox("Select document to inspect:", options=doc_options)

            if selected_option:
                sel_idx = int(selected_option.split(".")[0]) - 1
                selected_doc = ranked_docs[sel_idx]
                st.session_state["selected_document"] = selected_doc

                with st.expander(f"Full Metadata & Preview: {selected_doc['filename']}", expanded=True):
                    m_col1, m_col2, m_col3 = st.columns(3)
                    with m_col1:
                        st.write(f"**Filename:** `{selected_doc['filename']}`")
                    with m_col2:
                        st.write(f"**Document Type:** `{selected_doc['filetype']}`")
                    with m_col3:
                        st.write(f"**Similarity Score:** `{selected_doc['similarity_pct']}`")

                    st.markdown("**First 500 Characters:**")
                    st.info(selected_doc["preview"])
        else:
            st.info("No documents matched the current similarity threshold. Try lowering the threshold or using different keywords.")

    # Tab 2: Knowledge Graph & Entity Extraction
    with tab_graph:
        if not has_retrieval:
            st.info("Knowledge graph will appear after retrieving documents.")
        else:
            st.subheader("Extracted Domain Entities (Rule-Based Vocabulary Matching)")
            st.caption("Entities identified within the retrieved document text, color-coded by category:")
            render_entity_badges(extracted_entities)

            st.markdown("---")
            st.subheader("Interactive Knowledge Graph")
            st.caption("Directed graph synthesized from retrieved entities and predefined relational semantic triples.")

            # Legend Table
            with st.expander("View Category Color Legend & Active Edges", expanded=False):
                leg_col1, leg_col2 = st.columns(2)
                with leg_col1:
                    st.markdown(
                        """
                        **Node Category Color Code:**
                        - <span style='color:#2563EB; font-weight:bold;'>AI</span>: Artificial Intelligence, Machine Learning, Deep Learning, Neural Network, Robotics
                        - <span style='color:#16A34A; font-weight:bold;'>Domain</span>: Healthcare, Governance, Documents
                        - <span style='color:#EA580C; font-weight:bold;'>Technology</span>: Knowledge Graph, Information Retrieval, TF-IDF, Cosine Similarity, Algorithm, Data, Automation
                        - <span style='color:#9333EA; font-weight:bold;'>Ethics</span>: Ethics, Bias, Privacy
                        - <span style='color:#DC2626; font-weight:bold;'>Threat</span>: Cybersecurity, Malware, Detection
                        """,
                        unsafe_allow_html=True
                    )
                with leg_col2:
                    if active_edges:
                        st.write("**Active Relational Edges:**")
                        edges_df = pd.DataFrame(active_edges)
                        st.dataframe(edges_df, use_container_width=True, hide_index=True)
                    else:
                        st.info("No active relational triples formed for this query's entities.")

            # Render Graph
            if G is not None:
                fig_graph = render_graph_plotly(G, extracted_entities)
                st.plotly_chart(fig_graph, use_container_width=True)

    # Tab 3: Analytics Dashboard
    with tab_analytics:
        if not has_retrieval:
            st.info("Analytics will be generated after document retrieval.")
        else:
            st.subheader("Experimental Analytics Dashboard")

            # Streamlit metrics
            met1, met2, met3, met4, met5 = st.columns(5)
            with met1:
                st.metric("Total Documents Indexed", len(corpus_docs))
            with met2:
                st.metric("Retrieved Documents", len(ranked_docs))
            with met3:
                st.metric("Extracted Entities", len(extracted_entities))
            with met4:
                st.metric("Relationships", len(active_edges))
            with met5:
                avg_val = latest.get("average_similarity", latest.get("avg_similarity", 0.0))
                st.metric("Average Similarity", f"{avg_val * 100:.2f}%")

            st.divider()
            chart_col1, chart_col2 = st.columns(2)

            # Bar Chart: Top 10 entities by frequency
            with chart_col1:
                st.subheader("Top 10 Entities by Frequency")
                if extracted_entities:
                    top_entities = list(extracted_entities.items())[:10]
                    df_ent = pd.DataFrame(top_entities, columns=["Entity", "Frequency"])
                    fig_bar = px.bar(
                        df_ent,
                        x="Frequency",
                        y="Entity",
                        orientation="h",
                        color="Frequency",
                        color_continuous_scale="Blues"
                    )
                    fig_bar.update_layout(
                        title=dict(
                            text="Entity Occurrence in Retrieved Text",
                            font=dict(size=14)
                        ),
                        yaxis=dict(autorange="reversed"),
                        height=380,
                        margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No entities to display in frequency chart.")

            # Pie Chart: Document distribution by format
            with chart_col2:
                st.subheader("Corpus Document Distribution")
                if corpus_docs:
                    type_counts = {}
                    for d in corpus_docs:
                        ft = d.get("filetype", "UNKNOWN")
                        type_counts[ft] = type_counts.get(ft, 0) + 1
                    df_pie = pd.DataFrame(list(type_counts.items()), columns=["FileType", "Count"])
                    fig_pie = px.pie(
                        df_pie,
                        names="FileType",
                        values="Count",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    fig_pie.update_layout(
                        title=dict(
                            text="Indexed Document Formats",
                            font=dict(size=14)
                        ),
                        height=380,
                        margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("Corpus is empty.")

    # Tab 4: Trial Recording & CSV Export
    with tab_logger:
        st.subheader("Experimental Trial Recording")
        st.markdown(
            "Log the current retrieval run into your experimental session record. "
            "Record multiple trials with distinct queries, top-K thresholds, or document sets."
        )

        if "trials" not in st.session_state or st.session_state["trials"] is None:
            st.session_state["trials"] = []

        log_col1, log_col2 = st.columns([1.5, 3.5])

        with log_col1:
            st.write("**Record Current Run:**")
            curr_q = latest.get("query", "")
            if curr_q:
                st.write(f"- Query: *{curr_q[:30]}...*" if len(curr_q) > 30 else f"- Query: *{curr_q}*")
                st.write(f"- Retrieved: `{len(ranked_docs)}` documents")
                avg_val = latest.get("average_similarity", latest.get("avg_similarity", 0.0))
                st.write(f"- Avg Similarity: `{avg_val * 100:.2f}%`")
                st.write(f"- Entities: `{len(extracted_entities)}` | Edges: `{len(active_edges)}`")

                if st.button("Record Current Trial", type="primary", use_container_width=True):
                    trial_entry = {
                        "Trial #": len(st.session_state["trials"]) + 1,
                        "Timestamp": latest.get("timestamp", datetime.now().strftime("%H:%M:%S")),
                        "Query": curr_q,
                        "Top K": latest.get("top_k", top_k),
                        "Threshold": latest.get("threshold", threshold),
                        "Retrieved Count": len(ranked_docs),
                        "Average Similarity": f"{avg_val * 100:.2f}%",
                        "Entity Count": len(extracted_entities),
                        "Relationship Count": len(active_edges)
                    }
                    st.session_state["trials"].append(trial_entry)
                    st.toast(f"Trial #{trial_entry['Trial #']} successfully logged!")
            else:
                st.caption("No retrieval results to record. Run a search query first.")

            if st.button("Clear Logged Trials", use_container_width=True):
                st.session_state["trials"] = []
                st.toast("Trial log cleared.")

        with log_col2:
            st.write("**Session Trial Log Book:**")
            if st.session_state.get("trials"):
                df_trials = pd.DataFrame(st.session_state["trials"])
                st.dataframe(df_trials, use_container_width=True, hide_index=True)

                csv_bytes = df_trials.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Trials as CSV",
                    data=csv_bytes,
                    file_name="ir_kg_experiment_trials.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("No experimental trials recorded yet.")
