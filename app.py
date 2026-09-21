"""
Main Application Entrypoint for IIT Kharagpur Virtual Laboratory:
'Integration of Information Retrieval with Knowledge Graphs'

Provides modular navigation across:
1. Theory (Conceptual background, SVG Architecture, Objectives, Procedure, Applications)
2. Simulation (TF-IDF Retrieval, Knowledge Graph, Plotly Visualization, Analytics, Trial Logger)
3. Quiz (10 MCQs with instant automated feedback and score tracking)
4. Report Generation (Formal IIT-style PDF compilation and download)
"""

import streamlit as st
from theory import render_theory
from simulation import render_simulation, ensure_sample_documents
from quiz import render_quiz
from report import render_report


def init_session_state():
    """Initializes all necessary session state variables for the experiment."""
    if "trials" not in st.session_state:
        st.session_state["trials"] = []
    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state["quiz_submitted"] = False
    if "quiz_score" not in st.session_state:
        st.session_state["quiz_score"] = 0
    if "student_info" not in st.session_state:
        st.session_state["student_info"] = {
            "name": "Student Name",
            "roll": "20CS10001",
            "department": "Computer Science & Engineering",
            "date": ""
        }
    if "student_observations" not in st.session_state:
        st.session_state["student_observations"] = ""
    if "student_conclusion" not in st.session_state:
        st.session_state["student_conclusion"] = ""
    if "latest_retrieval" not in st.session_state or st.session_state["latest_retrieval"] is None:
        initial_empty = {
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
            "timestamp": ""
        }
        st.session_state["latest_retrieval"] = initial_empty
        st.session_state["latest_result"] = initial_empty
    if "latest_result" not in st.session_state or st.session_state["latest_result"] is None:
        st.session_state["latest_result"] = st.session_state["latest_retrieval"]
    if "selected_document" not in st.session_state:
        st.session_state["selected_document"] = None


def main():
    # Set page configuration
    st.set_page_config(
        page_title="IR & Knowledge Graphs Virtual Lab | IIT Kharagpur",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Pre-seed offline documents repository
    ensure_sample_documents("documents")

    # Initialize State
    init_session_state()

    # Main Experiment Header
    st.title("Integration of Information Retrieval with Knowledge Graphs")
    st.caption("IIT Kharagpur Virtual Laboratory | Department of Computer Science & Engineering")

    # Sidebar Navigation & Progress Tracker
    st.sidebar.title("Lab Navigation")
    section = st.sidebar.radio(
        "Select Experiment Module:",
        options=["Theory", "Simulation", "Quiz", "Report Generation"],
        index=1  # Default to Simulation for immediate interaction
    )

    st.sidebar.divider()
    st.sidebar.subheader("Experimental Progress Tracker")

    num_docs = len(st.session_state.get("corpus_docs", []))
    if num_docs == 0:
        # Check files on disk
        import os
        if os.path.exists("documents"):
            num_docs = len([f for f in os.listdir("documents") if os.path.isfile(os.path.join("documents", f))])

    num_trials = len(st.session_state.get("trials", []))
    quiz_done = st.session_state.get("quiz_submitted", False)

    col_side1, col_side2 = st.sidebar.columns(2)
    with col_side1:
        st.metric("Docs Indexed", num_docs)
    with col_side2:
        st.metric("Trials Logged", num_trials)

    if quiz_done:
        st.sidebar.success(f"Quiz Completed: {st.session_state.get('quiz_score', 0)} / 10")
    else:
        st.sidebar.info("Quiz Status: Pending")

    st.sidebar.markdown("---")
    st.sidebar.caption("Offline Virtual Laboratory System | Classical Information Retrieval & Graph Modeling")

    # Route to Selected Module
    if section == "Theory":
        render_theory()
    elif section == "Simulation":
        render_simulation()
    elif section == "Quiz":
        render_quiz()
    elif section == "Report Generation":
        render_report()


if __name__ == "__main__":
    main()
