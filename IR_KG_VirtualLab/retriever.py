"""
Information Retrieval Module using TF-IDF and Cosine Similarity.
Provides preprocessing, query expansion, vector indexing, and document ranking functions.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess(text: str) -> str:
    """
    Normalizes text before TF-IDF indexing and query matching.
    """
    text = text.lower()

    replacements = {
        "cyber security": "cybersecurity",
        "artificial intelligence": "ai",
        "machine-learning": "machine learning",
        "threat detection": "threat_detection",
        "network security": "network_security",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def build_index(documents: List[Dict[str, Any]]) -> Tuple[Optional[TfidfVectorizer], Optional[np.ndarray]]:
    """
    Builds TF-IDF inverted index matrix from loaded documents after applying preprocessing.
    
    Args:
        documents: List of document dicts with 'text' key.
        
    Returns:
        Tuple of (fitted TfidfVectorizer, document tfidf_matrix)
    """
    if not documents:
        return None, None

    corpus = [preprocess(doc.get("text", "")) for doc in documents]
    
    # Configure improved TF-IDF vectorizer according to specification
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=1
    )
    
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return vectorizer, tfidf_matrix


def retrieve(
    query: str,
    top_k: int,
    threshold: float,
    documents: List[Dict[str, Any]],
    vectorizer: Optional[TfidfVectorizer],
    tfidf_matrix: Optional[np.ndarray]
) -> List[Dict[str, Any]]:
    """
    Retrieves and ranks documents using cosine similarity between expanded query and corpus vectors.
    Workflow:
    1. Preprocess corpus (done at index time).
    2. Preprocess query.
    3. Expand query keywords.
    4. TF-IDF transform.
    5. Cosine similarity.
    6. Sort descending.
    7. Apply threshold.
    8. Return Top-K.
    
    Args:
        query: User input search text.
        top_k: Maximum number of ranked documents to return.
        threshold: Minimum similarity threshold (0.0 to 1.0).
        documents: List of document metadata dictionaries.
        vectorizer: Fitted TfidfVectorizer instance.
        tfidf_matrix: TF-IDF feature matrix of corpus.
        
    Returns:
        List of ranked document dictionaries with rich retrieval metadata.
    """
    if not query or not query.strip() or vectorizer is None or tfidf_matrix is None or not documents:
        return []

    # 1. Preprocess query
    normalized_query = preprocess(query).strip()
    if not normalized_query:
        return []

    # 2. Query expansion (internal only, displayed query remains unchanged)
    expanded_terms = [normalized_query]

    # If query contains "ai"
    if re.search(r"\bai\b", normalized_query) or "ai" in normalized_query.split():
        expanded_terms.append("artificial intelligence")

    # If query contains "cybersecurity"
    if "cybersecurity" in normalized_query:
        expanded_terms.append("malware intrusion detection threat network security")

    search_query = " ".join(expanded_terms)

    # 3. TF-IDF transform
    try:
        query_vec = vectorizer.transform([search_query])
    except Exception:
        return []

    # 4. Cosine similarity
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # 5. Sort descending
    sorted_indices = np.argsort(similarities)[::-1]

    # 6. Apply threshold
    threshold_docs = []
    for idx in sorted_indices:
        score = float(similarities[idx])
        if score >= threshold:
            threshold_docs.append({
                "doc_index": int(idx),
                "filename": documents[idx].get("filename", f"doc_{idx}"),
                "filetype": documents[idx].get("filetype", "UNKNOWN"),
                "text": documents[idx].get("text", ""),
                "similarity_score": score,
                "similarity": score,
                "similarity_pct": f"{score * 100:.2f}%",
                "preview": documents[idx].get("text", "")[:500]
            })

    # 7. Return Top-K
    ranked_results = []
    for rank, item in enumerate(threshold_docs[:top_k], start=1):
        item["rank"] = rank
        ranked_results.append(item)

    return ranked_results


def get_results_dataframe(ranked_results: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Converts ranked results into a display table with Rank, Document, and Similarity columns.
    """
    if not ranked_results:
        return pd.DataFrame(columns=["Rank", "Document", "Similarity"])

    data = []
    for r in ranked_results:
        sim_display = r.get("similarity_pct") or f"{r.get('similarity_score', 0.0) * 100:.2f}%"
        data.append({
            "Rank": r["rank"],
            "Document": r["filename"],
            "Similarity": sim_display
        })

    return pd.DataFrame(data)
