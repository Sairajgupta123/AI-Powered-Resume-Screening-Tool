from __future__ import annotations

import re
from pathlib import Path
from typing import List

import docx
import pdfplumber
import spacy
import nltk

_nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
_STOPWORDS = set(nltk.corpus.stopwords.words("english"))

_SKILL_DB = {
    "python", "java", "javascript", "c", "c++", "c#", "sql", "html", "css",
    "react", "angular", "vue", "django", "flask", "node", "express", "aws",
    "azure", "gcp", "docker", "kubernetes", "git", "tensorflow", "pytorch",
}

def _read_file(file_path: Path) -> str:
    """Extract raw text from PDF, DOCX or TXT file."""
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        with pdfplumber.open(str(file_path)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    if suffix in {".docx", ".doc"}:
        document = docx.Document(str(file_path))
        return "\n".join(p.text for p in document.paragraphs)

    if suffix == ".txt":
        return file_path.read_text(encoding="utf‑8", errors="ignore")

    raise ValueError(f"Unsupported file type: {file_path.suffix}")

def _normalize(text: str) -> str:
    """Lower‑case, lemmatize and remove stop‑words."""
    doc = _nlp(text.lower())
    tokens = [t.lemma_ for t in doc if t.is_alpha and t.text not in _STOPWORDS]
    return " ".join(tokens)

def _extract_skills(text: str) -> List[str]:
    """Simple keyword match against the skills database."""
    tokens = set(re.findall(r"\b[a-zA-Z\+#]{2,}\b", text.lower()))
    return sorted(tokens & _SKILL_DB)

def _guess_name(text: str) -> str | None:
    """Heuristic: first line containing two capitalised words."""
    for line in text.splitlines():
        line = line.strip()
        match = re.match(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", line)
        if match:
            return match.group(1)
    return None

def parse_resume(file_path: Path) -> dict:
    """Return a structured representation of the resume."""
    raw_text = _read_file(file_path)
    return {
        "filename": file_path.name,
        "name": _guess_name(raw_text),
        "skills": _extract_skills(raw_text),
        "raw_text": _normalize(raw_text),
    }
