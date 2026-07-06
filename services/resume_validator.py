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
]

EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s-]?)?\(?\d{3,4}\)?[\s-]?\d{3}[\s-]?\d{3,4}")
MIN_WORD_COUNT = 60          # very short/blank files are rejected
MIN_SIGNALS_REQUIRED = 2     # need at least this many resume signals to pass


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

    signals = 0
    matched_sections = [kw for kw in SECTION_KEYWORDS if kw in lower]
    if matched_sections:
        signals += 1

    has_email = bool(EMAIL_RE.search(cleaned))
    has_phone = bool(PHONE_RE.search(cleaned))
    if has_email:
        signals += 1
    if has_phone:
        signals += 1

    lines = [l for l in cleaned.split("\n") if l.strip()]
    if len(lines) >= 15:
        signals += 1

    off_topic_hits = sum(1 for kw in OFF_TOPIC_KEYWORDS if kw in lower)

    if off_topic_hits >= 2 and signals < MIN_SIGNALS_REQUIRED:
        return False, "This document doesn't look like a resume. Please upload your resume (PDF or DOCX)."

    if signals < MIN_SIGNALS_REQUIRED:
        return False, (
            "We couldn't recognize this as a resume — it doesn't contain typical resume "
            "sections (Experience, Education, Skills, etc.) or contact details. "
            "Please double-check the file and upload your resume."
        )

    return True, ""