
import re

SECTION_KEYWORDS = [
    "experience", "work experience", "employment", "professional experience",
    "education", "academic",
    "skills", "technical skills", "core competencies",
    "projects", "project experience",
    "certification", "certifications",
    "summary", "objective", "profile",
    "achievements", "accomplishments",
    "internship", "internships",
]

OFF_TOPIC_KEYWORDS = [
    "invoice", "purchase order", "terms and conditions", "chapter one",
    "table of contents", "abstract", "isbn", "recipe", "ingredients",
    "screenplay", "lorem ipsum",
    "pnr", "irctc", "gstin", "invoice number", "boarding at",
    "passenger details", "ticket fare", "booking status", "e-ticket",
    "reservation slip", "boarding pass", "flight no", "seat no",
    "order id", "transaction id", "amount payable", "grand total",
]

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s-]?)?\(?\d{3,4}\)?[\s-]?\d{3}[\s-]?\d{3,4}")
MIN_WORD_COUNT = 60          # very short/blank files are rejected


def is_valid_resume(text: str):
    """
    Returns (is_valid: bool, reason: str).
    reason is a short, user-facing explanation when is_valid is False.
    """
    if not text or not text.strip():
        return False, "We couldn't read any text from this file. Please upload a valid PDF or DOCX resume."

    cleaned = text.strip()
    word_count = len(cleaned.split())

    if word_count < MIN_WORD_COUNT:
        return False, "This file looks too short to be a resume. Please upload a complete resume."

    lower = cleaned.lower()

    off_topic_hits = sum(1 for kw in OFF_TOPIC_KEYWORDS if kw in lower)
    digit_ratio = sum(c.isdigit() for c in cleaned) / max(1, len(cleaned))


    if off_topic_hits >= 2 or digit_ratio > 0.15:
        return False, (
            "This looks like a ticket, invoice, or receipt rather than a resume. "
            "Please upload your resume (PDF or DOCX)."
        )

    has_section = any(kw in lower for kw in SECTION_KEYWORDS)


    if not has_section:
        return False, (
            "We couldn't recognize this as a resume — it doesn't contain typical resume "
            "sections (Experience, Education, Skills, etc.). "
            "Please double-check the file and upload your resume."
        )

    has_email = bool(EMAIL_RE.search(cleaned))
    has_phone = bool(PHONE_RE.search(cleaned))
    lines = [l for l in cleaned.split("\n") if l.strip()]
    line_dense = len(lines) >= 15


    if not (has_email or has_phone or line_dense):
        return False, (
            "This document doesn't look like a complete resume. "
            "Please double-check the file and upload your resume."
        )

    return True, ""