"""
Theory Module for Information Retrieval with Knowledge Graphs Virtual Lab.
Contains conceptual background, SVG system architecture, objectives, procedure, and applications.
"""

import streamlit as st
import streamlit.components.v1 as components


# SVG Architecture Diagram representing the complete IR + KG Pipeline
ARCHITECTURE_SVG = """
<div style="display: flex; justify-content: center; align-items: center; width: 100%; overflow-x: auto; margin: 0; padding: 0;">
<svg width="100%" height="280" viewBox="0 0 780 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 780px; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <linearGradient id="gradBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1D4ED8;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradOrange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F97316;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#C2410C;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="gradGreen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#10B981;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#047857;stop-opacity:1" />
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#64748B"/>
    </marker>
  </defs>

  <!-- Row 1: Document Processing to Retrieval -->
  <g transform="translate(20, 30)">
    <!-- Node 1: Documents -->
    <rect x="0" y="0" width="125" height="52" rx="8" fill="url(#gradBlue)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))" />
    <text x="62" y="24" text-anchor="middle" fill="#FFFFFF" font-weight="600" font-size="12">Document Corpus</text>
    <text x="62" y="40" text-anchor="middle" fill="#DBEAFE" font-size="10">PDF, DOCX, TXT, HTML</text>

    <!-- Arrow 1 -> 2 -->
    <path d="M 125 26 L 165 26" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)" />

    <!-- Node 2: TF-IDF Vectorizer -->
    <rect x="175" y="0" width="135" height="52" rx="8" fill="url(#gradBlue)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))" />
    <text x="242" y="24" text-anchor="middle" fill="#FFFFFF" font-weight="600" font-size="12">TF-IDF Vectorizer</text>
    <text x="242" y="40" text-anchor="middle" fill="#DBEAFE" font-size="10">Term Weight Matrix</text>

    <!-- Arrow 2 -> 3 -->
    <path d="M 310 26 L 350 26" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)" />

    <!-- Node 3: Cosine Similarity -->
    <rect x="360" y="0" width="135" height="52" rx="8" fill="url(#gradBlue)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))" />
    <text x="427" y="24" text-anchor="middle" fill="#FFFFFF" font-weight="600" font-size="12">Cosine Similarity</text>
    <text x="427" y="40" text-anchor="middle" fill="#DBEAFE" font-size="10">Vector Angle Match</text>

    <!-- Arrow 3 -> 4 -->
    <path d="M 495 26 L 535 26" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)" />

    <!-- Node 4: Top Ranked Docs -->
    <rect x="545" y="0" width="145" height="52" rx="8" fill="url(#gradBlue)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))" />
    <text x="617" y="24" text-anchor="middle" fill="#FFFFFF" font-weight="600" font-size="12">Top-K Retrieved Docs</text>
    <text x="617" y="40" text-anchor="middle" fill="#DBEAFE" font-size="10">Ranked Results</text>
  </g>

  <!-- Transition Arrow Down to Knowledge Graph Pipeline -->
  <path d="M 637 82 L 637 130 L 637 150" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)" />

  <!-- Row 2: Knowledge Extraction to Graph Generation -->
  <g transform="translate(140, 160)">
    <!-- Node 7: Knowledge Graph (Destination) -->
    <rect x="0" y="0" width="145" height="54" rx="8" fill="url(#gradGreen)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))" />
    <text x="72" y="24" text-anchor="middle" fill="#FFFFFF" font-weight="600" font-size="12">Knowledge Graph</text>
    <text x="72" y="42" text-anchor="middle" fill="#D1FAE5" font-size="10">Interactive Visual Graph</text>

    <!-- Arrow 6 -> 7 (Leftward) -->
    <path d="M 180 27 L 155 27" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)" />

    <!-- Node 6: Relationship Builder -->
    <rect x="190" y="0" width="145" height="54" rx="8" fill="url(#gradOrange)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))" />
    <text x="262" y="24" text-anchor="middle" fill="#FFFFFF" font-weight="600" font-size="12">Relationship Builder</text>
    <text x="262" y="42" text-anchor="middle" fill="#FFEDD5" font-size="10">Semantic Triples</text>

    <!-- Arrow 5 -> 6 (Leftward) -->
    <path d="M 370 27 L 345 27" stroke="#64748B" stroke-width="2" marker-end="url(#arrow)" />

    <!-- Node 5: Entity Extraction -->
    <rect x="380" y="0" width="145" height="54" rx="8" fill="url(#gradOrange)" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))" />
    <text x="452" y="24" text-anchor="middle" fill="#FFFFFF" font-weight="600" font-size="12">Entity Extraction</text>
    <text x="452" y="42" text-anchor="middle" fill="#FFEDD5" font-size="10">Vocabulary Matching</text>
  </g>
</svg>
</div>
"""


def render_theory():
    """Renders the comprehensive IIT Virtual Lab Theory Section."""
    st.header("Section 1: Theoretical Framework & Laboratory Manual")
    st.markdown(
        "Welcome to the **Integration of Information Retrieval with Knowledge Graphs** virtual experiment. "
        "This laboratory explores how traditional statistical information retrieval models are enhanced "
        "by structured knowledge representation and graph exploration."
    )

    # 1. Introduction
    st.subheader("1. Introduction to Information Retrieval (IR)")
    st.markdown(
        """
        **Information Retrieval (IR)** is the science of searching for relevant documents, structured or unstructured 
        information, and metadata within large collections of text. As institutional and enterprise repositories grow 
        exponentially, finding precise information rapidly is indispensable for research, medical diagnostics, 
        governance, and engineering decision-making.

        * **Why Document Retrieval is Important:**
          Modern text repositories contain millions of heterogeneous files (research papers, clinical reports, legal briefs). 
          Manual review is impossible; IR algorithms index document content and estimate which items satisfy an explicit user query.

        * **Traditional Keyword Search:**
          Early retrieval systems relied strictly on boolean logic (AND, OR, NOT) or raw keyword occurrences. While computationally 
          cheap, keyword search treats documents as disconnected bags of words without understanding underlying context.

        * **Limitations of Keyword Matching:**
          - **Synonymy:** Multiple words represent the same concept (e.g., *'Artificial Intelligence'* vs *'Machine Intelligence'*). 
            Queries missing the exact word fail to retrieve pertinent documents.
          - **Polysemy:** The same word carries distinct meanings in different contexts (e.g., *'Apple'* the fruit vs *'Apple'* the company).
          - **Lack of Relational Context:** Keyword matching cannot establish relations between entities (e.g., whether *'Ethics'* 
            regulates *'Bias'* or if *'Malware'* attacks *'Healthcare'*).
        """
    )

    # 2. Knowledge Graph
    st.subheader("2. Knowledge Graphs (KG)")
    st.markdown(
        """
        A **Knowledge Graph** represents a network of real-world entities—objects, situations, concepts, or events—and illustrates 
        the semantic relationship between them. Knowledge is organized as a directed multi-relational graph:

        * **Node (Vertex):** Represents an **Entity**, such as a concept (*Machine Learning*), system (*Cybersecurity*), 
          domain (*Healthcare*), or artifact (*Documents*).
        * **Edge (Link):** Represents a **Relationship (Predicate)** connecting two entities, indicating an action, 
          composition, or dependency (e.g., `(Healthcare) --[uses]--> (Artificial Intelligence)`).
        * **Entity:** A distinctly identifiable subject or object in the knowledge domain.
        * **Relationship:** Directed predicate linking subject to object, establishing semantic meaning.
        * **Graph Traversal:** Traversing interconnected nodes allows associative search, contextual reasoning, and multi-hop 
          inference that static documents cannot directly provide.
        """
    )

    # 3. Integration of IR + KG
    st.subheader("3. Integration of Information Retrieval with Knowledge Graphs")
    st.markdown(
        """
        While statistical IR algorithms (such as **TF-IDF** and **Cosine Similarity**) excel at ranking relevant documents based on 
        term frequencies, they produce flat linear lists of files. By integrating Knowledge Graphs:
        
        1. **Retrieved Documents Become Contextual Graphs:** The retrieved text is parsed to extract core domain entities.
        2. **Relational Synthesis:** Extracted entities are mapped against known relational patterns, generating an active subgraph.
        3. **Exploratory Navigation:** Users do not merely read search snippets; they visually explore interconnected domains, 
           understanding how retrieved ideas influence one another.
        """
    )

    # 4. Architecture
    st.subheader("4. System Architecture")
    st.markdown("The laboratory pipeline operates according to the modular architecture depicted below:")
    components.html(ARCHITECTURE_SVG, height=310, scrolling=False)
    st.caption("Figure 1: Modular Pipeline showing statistical retrieval coupled with rule-based entity and relationship synthesis.")

    # 5. Learning Objectives
    st.subheader("5. Learning Objectives")
    st.markdown(
        """
        Upon completion of this virtual laboratory experiment, students and researchers will be able to:
        1. **Understand and implement** Vector Space Models using TF-IDF representation and Cosine Similarity ranking.
        2. **Analyze the limitations** of raw keyword search when handling conceptual domain queries.
        3. **Extract semantic entities** systematically from heterogeneous documents (PDF, DOCX, TXT, HTML, PPTX).
        4. **Construct and visualize** a directed knowledge graph using NetworkX and interactive Plotly scatter coordinates.
        5. **Evaluate multi-relational graphs** to perform contextual information exploration and multi-domain link analysis.
        """
    )

    # 6. Experimental Procedure
    st.subheader("6. Experimental Procedure")
    st.markdown(
        """
        Follow these step-by-step instructions to conduct the experiment:
        - **Step 1:** Ensure test documents are placed in the `documents/` repository folder (the system scans automatically).
        - **Step 2:** Navigate to the **Simulation** tab from the left sidebar.
        - **Step 3:** Enter a search query representing your conceptual investigation (e.g., *"Artificial intelligence applications in healthcare"*).
        - **Step 4:** Select your retrieval parameters: **Top-K** documents (3 to 10) and **Cosine Similarity Threshold** (0.0 to 1.0).
        - **Step 5:** Click **Retrieve Documents** to execute vectorization and ranking.
        - **Step 6:** Inspect the ranked similarity table and expand individual document previews to examine extracted snippets.
        - **Step 7:** Examine the extracted entity badges and interact with the dynamically generated **Knowledge Graph**.
        - **Step 8:** Click **Record Current Trial** to save parameter metrics into your experimental session log.
        - **Step 9:** Proceed to the **Quiz** section to evaluate your conceptual grasp.
        - **Step 10:** Open **Report Generation**, review trial summaries, enter student details, and export the official **PDF Report**.
        """
    )

    # 7. Real-World Applications
    st.subheader("7. Real-World Applications")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            * **Healthcare & Biomedicine:**
              Linking patient clinical records with biomedical research graphs to correlate disease symptoms, 
              medications, and adverse side-effects.
            * **Cybersecurity & Threat Intelligence:**
              Correlating incident logs with threat knowledge graphs to uncover malware signatures, threat actors, 
              and attack vectors across distributed networks.
            * **Education & Adaptive Learning:**
              Structuring instructional curricula into prerequisite concept graphs to recommend targeted learning modules.
            """
        )

    with col2:
        st.markdown(
            """
            * **Digital Library & Archive Systems:**
              Enabling semantic discovery across centuries of historical and technical publications beyond simple author/title queries.
            * **Legal Search & Regulatory Compliance:**
              Traversing statutory codes, judicial precedents, and compliance mandates to analyze legal risk and regulatory alignment.
            """
        )
