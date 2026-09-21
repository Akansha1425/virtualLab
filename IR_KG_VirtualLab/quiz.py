"""
Quiz Module for Information Retrieval & Knowledge Graphs Virtual Lab.
Provides 10 comprehensive conceptual multiple-choice questions with automated grading and instant feedback.
"""

from typing import List, Dict, Any
import streamlit as st


QUIZ_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "topic": "TF-IDF",
        "question": "What does the Inverse Document Frequency (IDF) factor in TF-IDF primarily measure?",
        "options": [
            "A) The total character length of an individual document",
            "B) How rare or informative a term is across the entire document corpus",
            "C) The alphabetical rank of a query term in a lexicon",
            "D) The transmission speed of packets across a local network"
        ],
        "answer_index": 1,
        "explanation": "IDF penalizes common terms (like 'the', 'is') that occur in almost all documents and assigns higher weights to terms that appear in few documents, making them more discriminative."
    },
    {
        "id": 2,
        "topic": "Cosine Similarity",
        "question": "Why is Cosine Similarity preferred over Euclidean distance when comparing document vector representations?",
        "options": [
            "A) Cosine similarity is invariant to document length because it measures the angle between vectors rather than their magnitude",
            "B) Cosine similarity only works on integer values",
            "C) Euclidean distance cannot be calculated in spaces with more than two dimensions",
            "D) Cosine similarity always outputs negative numbers for similar texts"
        ],
        "answer_index": 0,
        "explanation": "Two documents discussing identical topics with different word counts (e.g., a short abstract vs a long thesis) produce vectors pointing in the same direction. Cosine similarity captures this orientation independent of vector length."
    },
    {
        "id": 3,
        "topic": "Information Retrieval",
        "question": "Which of the following is a major limitation of traditional Boolean keyword search in Information Retrieval?",
        "options": [
            "A) It cannot handle queries with more than two words",
            "B) It requires specialized quantum hardware to compute",
            "C) It suffers from vocabulary mismatch caused by synonymy and polysemy and cannot rank documents by relevance degree",
            "D) It converts all text documents into binary image files"
        ],
        "answer_index": 2,
        "explanation": "Boolean keyword search relies on exact token matching. It cannot retrieve documents using synonyms and does not produce graded relevance scores (a document either matches 100% or 0%)."
    },
    {
        "id": 4,
        "topic": "Knowledge Graph",
        "question": "In a formal Knowledge Graph, what foundational data structure is used to represent facts and assertions?",
        "options": [
            "A) Fixed-length circular queues",
            "B) Semantic triples of (Subject, Predicate, Object)",
            "C) Single-column relational database tables",
            "D) Unsorted binary search trees"
        ],
        "answer_index": 1,
        "explanation": "Knowledge graphs represent knowledge as semantic triples: (Subject, Predicate, Object), or (Head Entity, Relation, Tail Entity), forming directed graph networks."
    },
    {
        "id": 5,
        "topic": "Nodes",
        "question": "In the context of the knowledge graph constructed in this experiment, what does a 'Node' represent?",
        "options": [
            "A) A network cable connecting two physical servers",
            "B) An individual extracted entity or conceptual topic",
            "C) The total byte size of an uploaded PDF file",
            "D) A syntax error thrown by the Python interpreter"
        ],
        "answer_index": 1,
        "explanation": "Nodes in this domain represent extracted domain entities such as 'Artificial Intelligence', 'Cybersecurity', 'Healthcare', or 'TF-IDF'."
    },
    {
        "id": 6,
        "topic": "Edges",
        "question": "What information is encoded by a directed 'Edge' between two nodes in a knowledge graph?",
        "options": [
            "A) The exact time taken to compile the Python source code",
            "B) The semantic relationship or predicate that links the subject entity to the object entity",
            "C) The font size used to render the document title",
            "D) The physical distance between computer monitors"
        ],
        "answer_index": 1,
        "explanation": "Edges represent the directed relationships (predicates) connecting concepts, such as 'uses', 'detects', 'protects', or 'enhances'."
    },
    {
        "id": 7,
        "topic": "Entities",
        "question": "How does rule-based entity extraction identify key domain terms in retrieved documents without requiring pre-trained deep neural models?",
        "options": [
            "A) By randomly selecting words from the first paragraph",
            "B) By matching text tokens against a curated vocabulary dictionary using regular expressions and boundary detection",
            "C) By reading external Wikipedia API pages over an active internet connection",
            "D) By deleting all vowels and sorting the remaining consonants"
        ],
        "answer_index": 1,
        "explanation": "Rule-based entity extraction operates completely offline by matching document tokens against a defined domain lexicon with case-insensitive word boundary regex."
    },
    {
        "id": 8,
        "topic": "Relationships",
        "question": "Consider the relationship tuple: ('Healthcare', 'uses', 'Artificial Intelligence'). Which element serves as the predicate?",
        "options": [
            "A) 'Healthcare'",
            "B) 'uses'",
            "C) 'Artificial Intelligence'",
            "D) Both 'Healthcare' and 'Artificial Intelligence'"
        ],
        "answer_index": 1,
        "explanation": "In the triple (Subject, Predicate, Object), 'Healthcare' is the Subject, 'uses' is the Predicate (Relationship), and 'Artificial Intelligence' is the Object."
    },
    {
        "id": 9,
        "topic": "Contextual Search",
        "question": "How does augmenting Information Retrieval with Knowledge Graphs improve contextual exploration for a researcher?",
        "options": [
            "A) It permanently deletes irrelevant documents from the hard drive",
            "B) It transforms isolated retrieved documents into an interconnected web of concepts, revealing hidden connections and multi-hop paths",
            "C) It encrypts the user query to prevent other students from viewing it",
            "D) It increases the document file size by 500%"
        ],
        "answer_index": 1,
        "explanation": "Integrating KGs allows researchers to see not only which documents match keywords, but also how the concepts discussed within those documents relate to other domains."
    },
    {
        "id": 10,
        "topic": "Applications",
        "question": "In cybersecurity intelligence, how does a knowledge graph provide superior insight compared to flat keyword search on server log files?",
        "options": [
            "A) It speeds up the computer's CPU clock frequency directly",
            "B) It connects detected malware signatures to known threat actors, vulnerabilities, and targeted organizational assets",
            "C) It prevents physical theft of laptops from laboratory desks",
            "D) It replaces all passwords with one-digit numbers"
        ],
        "answer_index": 1,
        "explanation": "In threat intelligence, security knowledge graphs correlate disparate indicators of compromise (IP addresses, malware hashes, vulnerability CVEs) to expose entire multi-stage attack campaigns."
    }
]


def render_quiz():
    """Renders Section 3: Assessment Quiz with Self-Grading and Feedback."""
    st.header("Section 3: Conceptual Assessment Quiz")
    st.markdown(
        "Evaluate your understanding of **Information Retrieval, TF-IDF, Vector Space Models, and Knowledge Graph Architecture**."
    )

    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state["quiz_submitted"] = False
    if "quiz_score" not in st.session_state:
        st.session_state["quiz_score"] = 0

    with st.form("ir_kg_quiz_form"):
        user_responses = {}
        for q in QUIZ_QUESTIONS:
            st.subheader(f"Question {q['id']}: [{q['topic']}]")
            st.write(q["question"])
            selected = st.radio(
                label=f"Options for Question {q['id']}:",
                options=q["options"],
                index=st.session_state["quiz_answers"].get(q["id"], 0),
                key=f"quiz_radio_{q['id']}",
                label_visibility="collapsed"
            )
            user_responses[q["id"]] = q["options"].index(selected)
            st.markdown("---")

        submitted = st.form_submit_button("Submit Quiz for Evaluation", type="primary")

    if submitted:
        score = 0
        st.session_state["quiz_answers"] = user_responses
        st.session_state["quiz_submitted"] = True

        st.divider()
        st.subheader("Quiz Evaluation & Detailed Explanations")
        for q in QUIZ_QUESTIONS:
            user_ans = user_responses.get(q["id"])
            correct_ans = q["answer_index"]
            if user_ans == correct_ans:
                score += 1
                st.success(f"**Question {q['id']} ({q['topic']}): Correct!**\n\n_{q['explanation']}_")
            else:
                st.error(
                    f"**Question {q['id']} ({q['topic']}): Incorrect.**\n\n"
                    f"Your answer: **{q['options'][user_ans]}**\n\n"
                    f"**Correct Answer:** **{q['options'][correct_ans]}**\n\n"
                    f"**Explanation:** _{q['explanation']}_"
                )

        st.session_state["quiz_score"] = score
        perc = (score / len(QUIZ_QUESTIONS)) * 100
        st.info(f"Final Assessment Score: **{score} / {len(QUIZ_QUESTIONS)}** ({perc:.1f}%)")

    elif st.session_state.get("quiz_submitted", False):
        score = st.session_state.get("quiz_score", 0)
        perc = (score / len(QUIZ_QUESTIONS)) * 100
        st.success(f"Assessment completed. Your recorded score: **{score} / {len(QUIZ_QUESTIONS)}** ({perc:.1f}%)")
