"""Session-state defaults for the whole app."""
import uuid
import streamlit as st

def init_session():
    defaults = {
        "page":               "home",
        "session_id":         str(uuid.uuid4()),
        "resume_data":        None,
        "questions":          [],
        "personalized":       False,
        "role":               "Software Engineer",
        "current_q_index":    0,
        "answers":            {},
        "evaluations":        {},
        "current_eval":       None,
        "interview_started":  False,
        "interview_complete": False,
        "upload_error":       None,
        "q_start_time":       None,
        "career_recommendations": None,
        "roadmap_data":       None,
        "job_description":    "",
        "job_match_result":   None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
