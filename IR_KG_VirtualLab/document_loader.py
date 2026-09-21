"""
Document Loader Module for Information Retrieval & Knowledge Graph Virtual Lab.
Supports recursive scanning and text extraction from:
- PDF (via PyPDF2)
- DOCX (via python-docx)
- TXT (UTF-8 standard)
- HTML/HTM (via html.parser)
- PPTX/PPT (via zipfile and XML parsing)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from typing import List, Dict, Any


class HTMLTextExtractor(HTMLParser):
    """Simple, robust HTML tag stripper using Python's standard library."""
    def __init__(self):
        super().__init__()
        self.text_parts: List[str] = []

    def handle_data(self, data: str):
        text = data.strip()
        if text:
            self.text_parts.append(text)

    def get_text(self) -> str:
        return " ".join(self.text_parts)


def _extract_txt(file_path: str) -> str:
    """Extract text from plain text files with encoding fallback."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1", errors="ignore") as f:
            return f.read()


def _extract_html(file_path: str) -> str:
    """Extract text from HTML files by stripping markup tags."""
    content = _extract_txt(file_path)
    parser = HTMLTextExtractor()
    parser.feed(content)
    return parser.get_text()


def _extract_pdf(file_path: str) -> str:
    """Extract text from PDF files using PyPDF2."""
    try:
        import PyPDF2
        text_parts = []
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_parts.append(extracted)
        return "\n".join(text_parts)
    except Exception as e:
        return f"[PDF Extraction Error: {e}]"


def _extract_docx(file_path: str) -> str:
    """Extract text from DOCX files using python-docx."""
    try:
        import docx
        doc = docx.Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        return f"[DOCX Extraction Error: {e}]"


def _extract_pptx(file_path: str) -> str:
    """
    Extract text from PPTX files using standard library zipfile and XML parsing.
    Scans ppt/slides/slide*.xml and extracts all text nodes.
    """
    try:
        text_parts = []
        with zipfile.ZipFile(file_path, "r") as z:
            # Slides are typically named ppt/slides/slide1.xml, slide2.xml, etc.
            slide_entries = [name for name in z.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")]
            # Sort slides naturally if possible
            slide_entries.sort()
            for slide_name in slide_entries:
                xml_bytes = z.read(slide_name)
                root = ET.fromstring(xml_bytes)
                for elem in root.iter():
                    # Look for drawingML text elements: tag ends with '}t' or is 't'
                    if elem.tag.endswith("}t") or elem.tag == "t":
                        if elem.text and elem.text.strip():
                            text_parts.append(elem.text.strip())
        return " ".join(text_parts)
    except Exception:
        # Fallback for binary or legacy files: attempt string extraction
        try:
            with open(file_path, "rb") as f:
                raw = f.read().decode("latin-1", errors="ignore")
                # Filter printable ascii segments
                words = [w for w in raw.split() if len(w) > 3 and w.isprintable()]
                return " ".join(words[:200])
        except Exception as e:
            return f"[Presentation Extraction Error: {e}]"


def load_documents(folder_path: str) -> List[Dict[str, Any]]:
    """
    Recursively scans the folder and extracts text from supported document types.
    
    Supported formats:
    - .pdf
    - .docx
    - .txt
    - .html / .htm
    - .ppt / .pptx
    
    Returns:
        List of dicts:
        [
            {
                "filename": str,
                "filetype": str,
                "path": str,
                "text": str
            },
            ...
        ]
    """
    documents: List[Dict[str, Any]] = []

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        return documents

    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            _, ext = os.path.splitext(filename)
            ext_clean = ext.lower().lstrip(".")

            text = ""
            filetype = ext_clean.upper()

            if ext_clean == "txt":
                text = _extract_txt(file_path)
            elif ext_clean in ("html", "htm"):
                text = _extract_html(file_path)
            elif ext_clean == "pdf":
                text = _extract_pdf(file_path)
            elif ext_clean == "docx":
                text = _extract_docx(file_path)
            elif ext_clean in ("pptx", "ppt"):
                text = _extract_pptx(file_path)
            else:
                # Unsupported extension
                continue

            cleaned_text = text.strip()
            if cleaned_text:
                documents.append({
                    "filename": filename,
                    "filetype": filetype,
                    "path": file_path,
                    "text": cleaned_text
                })

    return documents
