from datetime import datetime, timezone

def resume_doc(session_id, filename, raw_text, role, sections,
               found_skills, missing_skills, ats_score, score_label,
               suggestions, strengths, weaknesses, top_skills, summary):
    return {
        "session_id": session_id, "filename": filename, "raw_text": raw_text,
        "role": role, "sections": sections, "found_skills": found_skills,
        "missing_skills": missing_skills, "ats_score": ats_score,
        "score_label": score_label, "suggestions": suggestions,
        "strengths": strengths, "weaknesses": weaknesses,
        "top_skills": top_skills, "summary": summary,
        "created_at": datetime.now(timezone.utc),
    }

def interview_doc(session_id, role, questions, personalized=False):
    return {
        "session_id": session_id, "role": role, "questions": questions,
        "personalized": personalized, "answers": {}, "evaluations": {},
        "current_index": 0, "status": "in_progress",
        "started_at": datetime.now(timezone.utc), "completed_at": None,
    }

def history_doc(session_id, role, ats_score, interview_score,
                total_questions, attempted, accuracy, breakdown, summary):
    return {
        "session_id": session_id, "role": role, "ats_score": ats_score,
        "interview_score": interview_score, "total_questions": total_questions,
        "attempted": attempted, "accuracy": accuracy, "breakdown": breakdown,
        "summary": summary, "created_at": datetime.now(timezone.utc),
    }