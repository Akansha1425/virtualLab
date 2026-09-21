"""
Report Generation Module for Information Retrieval & Knowledge Graphs Virtual Lab.
Compiles student details, experimental parameters, latest retrieval records,
trials summary, observations, conclusion, and quiz scores into an official IIT-style PDF report.
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
import streamlit as st
from fpdf import FPDF


def clean_pdf_text(text: Any) -> str:
    """Sanitizes text strings to prevent latin-1 encoding errors in standard FPDF."""
    if text is None:
        return ""
    s = str(text)
    # Replace common typographic unicode characters with ASCII equivalents
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u2192": "->",
        "\u2022": "-",
        "\u00a0": " "
    }
    for orig, rep in replacements.items():
        s = s.replace(orig, rep)
    # Filter non-latin-1 characters
    return s.encode("latin-1", errors="replace").decode("latin-1")


class IITVirtualLabPDF(FPDF):
    """Custom FPDF layout for IIT Kharagpur Virtual Laboratory experiment reporting."""
    def header(self):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(24, 43, 73)
        self.cell(0, 7, "IIT KHARAGPUR VIRTUAL LABORATORY", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, "Department of Computer Science & Engineering | Information Retrieval & Knowledge Graphs", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.4)
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | Virtual Lab Report - IR & Knowledge Graphs", align="C")


def build_pdf_report(
    student_name: str,
    roll_number: str,
    department: str,
    date_str: str,
    trials_df: pd.DataFrame,
    latest_retrieval: Optional[Dict[str, Any]],
    observations: str,
    conclusion: str,
    quiz_score: int,
    quiz_total: int
) -> bytes:
    """
    Generates an official multi-section PDF report according to IIT Virtual Lab standards.
    """
    pdf = IITVirtualLabPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Document Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, clean_pdf_text("Experiment: Integration of Information Retrieval with Knowledge Graphs"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    # Student & Session Info Box
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, pdf.get_y(), 190, 24, "FD")
    y_start = pdf.get_y() + 2

    pdf.set_xy(14, y_start)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(28, 5, "Student Name:", 0)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(62, 5, clean_pdf_text(student_name or "N/A"), 0)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(28, 5, "Roll Number:", 0)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(62, 5, clean_pdf_text(roll_number or "N/A"), 1)

    pdf.set_xy(14, y_start + 7)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(28, 5, "Department:", 0)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(62, 5, clean_pdf_text(department or "N/A"), 0)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(28, 5, "Experiment Date:", 0)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(62, 5, clean_pdf_text(date_str or datetime.now().strftime("%Y-%m-%d")), 1)

    pdf.set_xy(14, y_start + 14)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(28, 5, "Quiz Evaluation:", 0)
    pdf.set_font("Helvetica", "B", 8)
    if quiz_score >= max(1, quiz_total // 2):
        pdf.set_text_color(16, 185, 129)
    else:
        pdf.set_text_color(220, 38, 38)
    perc = int((quiz_score / quiz_total) * 100 if quiz_total else 0)
    pdf.cell(62, 5, f"{quiz_score} / {quiz_total} ({perc}%)", 0)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(28, 5, "Status:", 0)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(62, 5, "Completed", 1)

    pdf.set_y(y_start + 24)
    pdf.ln(3)

    # 1. Aim & Objectives
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "1. Aim & Learning Objectives", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(10, 5, "Aim: ", 0)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, clean_pdf_text("Combine document retrieval results with graph-based entity and relationship exploration."), new_x="LMARGIN", new_y="NEXT")

    objectives = [
        "Index heterogeneous documents (PDF, DOCX, TXT, HTML, PPTX) into a Vector Space Model using TF-IDF.",
        "Calculate Cosine Similarity to score, rank, and retrieve relevant documents based on user query.",
        "Perform offline rule-based entity extraction and frequency analysis across retrieved texts.",
        "Synthesize semantic relationships into an interactive directed Knowledge Graph with NetworkX.",
        "Explore multi-relational concept paths to evaluate conceptual overlap and domain connections."
    ]
    for obj in objectives:
        pdf.cell(5, 4, "-", 0)
        pdf.cell(0, 4, clean_pdf_text(f" {obj}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # 2. Latest Retrieval Summary
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "2. Latest Information Retrieval & Graph Generation Execution", new_x="LMARGIN", new_y="NEXT")

    if latest_retrieval and latest_retrieval.get("query"):
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(28, 5, "Active Query:", 0)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 5, clean_pdf_text(f'"{latest_retrieval.get("query")}"'), new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(28, 5, "Parameters:", 0)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(0, 5, f"Top-K = {latest_retrieval.get('top_k', 'N/A')} | Cosine Threshold = {latest_retrieval.get('threshold', 'N/A')}", new_x="LMARGIN", new_y="NEXT")

        # Retrieved docs mini-table
        ret_docs = latest_retrieval.get("retrieved_docs", [])
        if ret_docs:
            pdf.ln(1)
            pdf.set_fill_color(37, 99, 235)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(16, 5, "Rank", 1, 0, "C", True)
            pdf.cell(110, 5, "Document Name", 1, 0, "L", True)
            pdf.cell(32, 5, "Type", 1, 0, "C", True)
            pdf.cell(32, 5, "Similarity", 1, 1, "C", True)

            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(30, 41, 59)
            fill = False
            for d in ret_docs[:5]:
                pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
                pdf.cell(16, 5, str(d.get("rank", "")), 1, 0, "C", fill)
                pdf.cell(110, 5, clean_pdf_text(d.get("filename", ""))[:55], 1, 0, "L", fill)
                pdf.cell(32, 5, str(d.get("filetype", "")), 1, 0, "C", fill)
                pdf.cell(32, 5, str(d.get("similarity_pct", "")), 1, 1, "C", fill)
                fill = not fill

        # Extracted entities and relationships summary
        entities = latest_retrieval.get("extracted_entities", {})
        if entities:
            pdf.ln(1)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(51, 65, 85)
            pdf.cell(35, 5, "Extracted Entities:", 0)
            pdf.set_font("Helvetica", "", 8)
            ent_summary = ", ".join([f"{k} ({v})" for k, v in list(entities.items())[:8]])
            pdf.cell(0, 5, clean_pdf_text(ent_summary), new_x="LMARGIN", new_y="NEXT")

        edges = latest_retrieval.get("active_edges", [])
        if edges:
            pdf.set_font("Helvetica", "B", 8)
            pdf.cell(35, 5, "Knowledge Graph Edges:", 0)
            pdf.set_font("Helvetica", "", 8)
            edge_summary = "; ".join([f"({e['source']} -[{e['relation']}]-> {e['target']})" for e in edges[:4]])
            pdf.multi_cell(0, 5, clean_pdf_text(edge_summary))
    else:
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 5, "No query execution captured yet in simulation session.", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(2)

    # 3. Recorded Experimental Trials
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "3. Experimental Trials Record Table", new_x="LMARGIN", new_y="NEXT")

    if trials_df.empty:
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 5, "No experimental trials logged during this session.", new_x="LMARGIN", new_y="NEXT")
    else:
        pdf.set_fill_color(37, 99, 235)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 7)

        cols = list(trials_df.columns)
        col_w = max(18, int(190 / max(1, len(cols))))

        for c in cols:
            pdf.cell(col_w, 5, clean_pdf_text(str(c))[:14], 1, 0, "C", True)
        pdf.ln()

        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(30, 41, 59)
        fill = False

        for _, row in trials_df.iterrows():
            pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
            for c in cols:
                val = row[c]
                val_str = f"{val:.2f}" if isinstance(val, float) else str(val)
                pdf.cell(col_w, 5, clean_pdf_text(val_str)[:15], 1, 0, "C", fill)
            pdf.ln()
            fill = not fill

    pdf.ln(3)

    # 4. Student Observations & Analysis
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "4. Experimental Observations", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(51, 65, 85)
    obs_text = observations.strip() if observations.strip() else (
        "Documents were retrieved with TF-IDF cosine similarity scores matching the semantic domain of the query. "
        "The rule-based entity extraction identified key topics, and the knowledge graph visualized meaningful relational links."
    )
    pdf.multi_cell(0, 4.5, clean_pdf_text(obs_text))
    pdf.ln(2)

    # 5. Conclusion
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 6, "5. Conclusion", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(51, 65, 85)
    conc_text = conclusion.strip() if conclusion.strip() else (
        "Integrating statistical Information Retrieval with Knowledge Graphs bridges unstructured document ranking "
        "with semantic contextual exploration. This enables researchers to trace concept dependencies across multi-domain datasets."
    )
    pdf.multi_cell(0, 4.5, clean_pdf_text(conc_text))
    pdf.ln(6)

    # Sign-off Line
    pdf.set_draw_color(180, 180, 180)
    y_sig = pdf.get_y() + 5
    if y_sig > 265:
        pdf.add_page()
        y_sig = 25
    pdf.line(130, y_sig, 195, y_sig)
    pdf.set_xy(130, y_sig + 2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(65, 4, "Student / Faculty Evaluator Signature", align="C")

    return bytes(pdf.output())


def render_report():
    """Renders Section 4: Dynamic Report Generation and Export."""
    st.header("Section 4: Laboratory Report Generation")
    st.markdown(
        "Generate a formal **IIT Kharagpur Virtual Laboratory Report** documenting your retrieval parameters, "
        "knowledge graph extractions, experimental trials, and quiz evaluation."
    )

    if "student_info" not in st.session_state:
        st.session_state["student_info"] = {
            "name": "Student Name",
            "roll": "20CS10001",
            "department": "Computer Science & Engineering",
            "date": str(datetime.now().date())
        }

    # Student Details Form
    st.subheader("1. Student & Institutional Credentials")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        name = st.text_input("Student Name", value=st.session_state["student_info"].get("name", "Student Name"))
    with col2:
        roll = st.text_input("Roll Number", value=st.session_state["student_info"].get("roll", "20CS10001"))
    with col3:
        dept = st.text_input("Department", value=st.session_state["student_info"].get("department", "Computer Science & Engineering"))
    with col4:
        lab_date = st.date_input("Experiment Date", value=datetime.now())

    st.session_state["student_info"]["name"] = name
    st.session_state["student_info"]["roll"] = roll
    st.session_state["student_info"]["department"] = dept
    st.session_state["student_info"]["date"] = str(lab_date)

    st.divider()

    # Observations and Conclusions
    st.subheader("2. Experimental Observations & Analytical Findings")
    observations = st.text_area(
        "Enter your observations on retrieval precision, entity extraction, and graph connectivity:",
        value=st.session_state.get(
            "student_observations",
            "Observed that increasing the similarity threshold reduced the number of retrieved documents but significantly enhanced topic precision. The knowledge graph synthesized multi-hop semantic links between healthcare and machine learning."
        ),
        height=100
    )
    st.session_state["student_observations"] = observations

    st.subheader("3. Conclusion")
    conclusion = st.text_area(
        "Enter your experimental conclusion:",
        value=st.session_state.get(
            "student_conclusion",
            "The integration of TF-IDF retrieval with knowledge graphs allows transitioning from isolated document retrieval to comprehensive conceptual exploration, demonstrating significant utility for research repositories."
        ),
        height=80
    )
    st.session_state["student_conclusion"] = conclusion

    st.divider()

    # Report Preview Details
    trials = st.session_state.get("trials", [])
    trials_df = pd.DataFrame(trials) if trials else pd.DataFrame()
    latest_retrieval = st.session_state.get("latest_retrieval", None)

    st.subheader("4. Summary Preview")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("Recorded Trials", len(trials))
    with p2:
        score = st.session_state.get("quiz_score", 0)
        st.metric("Quiz Score", f"{score} / 10")
    with p3:
        last_query = latest_retrieval.get("query", "None") if latest_retrieval else "None"
        st.metric("Last Query", last_query[:20] + "..." if len(last_query) > 20 else last_query)

    if not trials_df.empty:
        st.caption("Logged Experimental Trials to be included in PDF:")
        st.dataframe(trials_df, use_container_width=True, hide_index=True)
    else:
        st.info("No trials recorded in the Simulation tab yet. Your report will indicate 0 recorded trials.")

    # Generate PDF Report
    pdf_bytes = build_pdf_report(
        student_name=name,
        roll_number=roll,
        department=dept,
        date_str=str(lab_date),
        trials_df=trials_df,
        latest_retrieval=latest_retrieval,
        observations=observations,
        conclusion=conclusion,
        quiz_score=st.session_state.get("quiz_score", 0),
        quiz_total=10
    )

    st.divider()
    st.subheader("5. Official Lab Report Document")

    st.markdown(
        """
        **Generated Report Includes**

        * Student Details
        * Experiment Title
        * Aim & Objectives
        * Latest Retrieval Results
        * Knowledge Graph Summary
        * Trial Records
        * Observations
        * Conclusion
        * Quiz Score
        """
    )

    st.download_button(
        label="📄 Download Experiment Report (PDF)",
        data=pdf_bytes,
        file_name="IR_KG_VirtualLab_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
