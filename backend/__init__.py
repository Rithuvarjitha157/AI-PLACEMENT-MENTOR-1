"""
Resume Parser Service.

Extracts raw text from an uploaded PDF resume using PyMuPDF (fitz).
"""
import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> str:
    """Extracts and returns all text content from a PDF file."""
    text_chunks = []
    with fitz.open(file_path) as doc:
        for page in doc:
            text_chunks.append(page.get_text())
    return "\n".join(text_chunks).strip()


def quick_keyword_scan(resume_text: str) -> dict:
    """
    Lightweight, deterministic keyword scan used as a fallback / supplement
    to the LLM analysis. Helps demo work even if AI call fails.
    """
    text_lower = resume_text.lower()

    languages = ["python", "java", "c++", "c", "javascript", "typescript", "dart",
                 "go", "kotlin", "swift", "sql", "r", "rust"]
    frameworks = ["flutter", "react", "flask", "django", "node.js", "express",
                  "spring boot", "tensorflow", "pytorch", "firebase", "docker",
                  "kubernetes", "aws", "git", "mongodb", "postgresql", "mysql"]

    found_languages = [l for l in languages if l in text_lower]
    found_frameworks = [f for f in frameworks if f in text_lower]

    has_internship = any(k in text_lower for k in ["intern", "internship"])
    has_projects = any(k in text_lower for k in ["project", "built", "developed"])
    has_certifications = any(k in text_lower for k in ["certification", "certified", "certificate"])
    has_dsa = any(k in text_lower for k in ["data structures", "algorithms", "leetcode", "dsa"])

    return {
        "found_languages": found_languages,
        "found_frameworks": found_frameworks,
        "has_internship": has_internship,
        "has_projects": has_projects,
        "has_certifications": has_certifications,
        "has_dsa": has_dsa,
    }
