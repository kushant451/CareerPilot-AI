"""Best-effort persistence helpers. Each save is wrapped so a Mongo hiccup never breaks the UI."""
import streamlit as st

def save_resume_to_db():
    try:
        from database.resume_collection import delete_resume, save_resume
        sid = st.session_state.session_id
        r   = st.session_state.resume_data
        delete_resume(sid)
        save_resume(
            session_id=sid, filename=r.get("filename",""),
            raw_text=r.get("raw_text",""), role=r.get("role",""),
            sections=r.get("sections",{}), found_skills=r.get("found_skills",[]),
            missing_skills=r.get("missing_skills",[]), ats_score=r.get("ats_score",0),
            score_label=r.get("score_label",""), suggestions=r.get("suggestions",[]),
            strengths=r.get("strengths",[]), weaknesses=r.get("weaknesses",[]),
            top_skills=r.get("top_skills",[]), summary=r.get("summary",""),
        )
    except Exception:
        pass


def save_career_rec_to_db(result):
    try:
        from database.career_collection import save_career_recommendation
        save_career_recommendation(
            session_id=st.session_state.session_id,
            role=result.get("primary_role", ""),
            top_matches=result.get("top_matches", []),
            insight=result.get("insight", ""),
        )
    except Exception:
        pass


def save_roadmap_to_db(result):
    try:
        from database.career_collection import save_roadmap
        save_roadmap(
            session_id=st.session_state.session_id,
            role=result.get("role", ""),
            weeks=result.get("weeks", 0),
            milestones=result.get("milestones", []),
            total_skills=result.get("total_skills", 0),
            generated_by_ai=result.get("generated_by_ai", False),
        )
    except Exception:
        pass


def save_job_match_to_db(role, job_description, result):
    try:
        from database.career_collection import save_job_match
        save_job_match(
            session_id=st.session_state.session_id,
            role=role,
            job_description=job_description,
            match_percent=result.get("match_percent", 0),
            matched_keywords=result.get("matched_keywords", []),
            missing_keywords=result.get("missing_keywords", []),
            summary=result.get("summary", ""),
        )
    except Exception:
        pass
