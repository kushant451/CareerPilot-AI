"""Home / landing page: resume upload entry point."""
import os
import tempfile
import streamlit as st

from ui.widgets import svg_ring, avg_score
from ui.db_helpers import save_resume_to_db

def page_home():
    from config.settings import ROLES

    st.markdown("""
    <div style="text-align:center; padding:18px 0 32px">
        <div style="font-size:52px; margin-bottom:8px">👋</div>
        <h1 style="color:#3A2E2A; font-size:48px; font-weight:800; margin:0 0 10px">Welcome back</h1>
        <p style="color:#9C7A6B; font-size:20px; margin:0">Let's crack your dream job!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.upload_error:
        st.error(st.session_state.upload_error)
        st.session_state.upload_error = None

    col_form, col_ring = st.columns([3, 1])
    with col_form:
        st.markdown('<div class="ai-card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:28px;font-weight:700;color:#3A2E2A;margin-bottom:6px">🎯 Your AI Interview Coach</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#9C7A6B;font-size:20px;margin-bottom:16px">Upload your resume, check ATS score, practice interviews and improve your skills.</p>', unsafe_allow_html=True)

        role_sel  = st.selectbox("Target role", ROLES, key="home_role")
        uploaded  = st.file_uploader("Resume (PDF / DOCX)", type=["pdf","docx"], key="home_upload")

        if st.button("⬆️ Upload & Analyse Resume", type="primary", use_container_width=True):
            if uploaded:
                _process_resume(uploaded, role_sel)
            else:
                st.session_state.upload_error = "Please select a PDF or DOCX file first."
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ring:
        resume = st.session_state.resume_data
        pct    = 0
        if resume:
            pct = 50
            if st.session_state.interview_started:  pct += 30
            if st.session_state.evaluations:        pct += 20
        ats = resume.get("ats_score", 0) if resume else 0
        st.markdown(f"""
        <div class="ai-card-flat" style="text-align:center; margin-top:6px">
          <div style="font-size:11.5px;color:#9C7A6B;font-weight:600;text-transform:uppercase;
                      letter-spacing:.4px;margin-bottom:10px">Overall Progress</div>
          {svg_ring(pct, 100, size=90, color="#E8896A", sub="%")}
          <div style="margin-top:10px;display:flex;flex-direction:column;gap:5px">
            <div style="display:flex;justify-content:space-between;font-size:12.5px;color:#9C7A6B">
              <span>● ATS</span>
              <span style="color:#3A2E2A;font-weight:600">{ats}/100</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:12.5px;color:#9C7A6B">
              <span>● Score</span>
              <span style="color:#3A2E2A;font-weight:600">{avg_score()}/10</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#F0DDD0;margin:22px 0"></div>', unsafe_allow_html=True)

    resume     = st.session_state.resume_data
    ats_score  = resume.get("ats_score", 0)         if resume else 0
    slabel     = resume.get("score_label","—")       if resume else "Upload resume first"
    int_score  = avg_score()
    has_resume = resume is not None

    c1, c2, c3 = st.columns(3)
    with c1:
        color = "#10B981" if ats_score >= 70 else "#F59E0B" if ats_score >= 50 else "#EF4444"
        badge = "b-green" if ats_score >= 70 else "b-yellow" if ats_score >= 50 else "b-red"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;
                      letter-spacing:.4px;margin-bottom:6px">ATS Score</div>
          <div style="font-size:31px;font-weight:700;color:{color};margin-bottom:8px">
            {ats_score}<span style="font-size:15px;color:#9C7A6B">/100</span></div>
          <span class="{badge}">{slabel}</span>
        </div>""", unsafe_allow_html=True)
        if has_resume and st.button("View ATS Details →", key="h_ats"):
            st.session_state.page = "ats"; st.rerun()

    with c2:
        badge2 = "b-green" if st.session_state.interview_started else "b-yellow"
        label2 = "Completed" if st.session_state.interview_started else "Not started"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;
                      letter-spacing:.4px;margin-bottom:6px">Mock Score</div>
          <div style="font-size:31px;font-weight:700;color:#E8896A;margin-bottom:8px">
            {int_score}<span style="font-size:15px;color:#9C7A6B">/10</span></div>
          <span class="{badge2}">{label2}</span>
        </div>""", unsafe_allow_html=True)
        if st.session_state.interview_started:
            if st.button("View Report →", key="h_rep"):
                st.session_state.page = "report"; st.rerun()
        else:
            if st.button("Start Now →", key="h_start"):
                st.session_state.page = "questions"; st.rerun()

    with c3:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;letter-spacing:.4px;margin-bottom:12px">Quick Actions</div>', unsafe_allow_html=True)
        if st.button("📄 ATS Checker",        key="qa1", use_container_width=True): st.session_state.page="ats";       st.rerun()
        if st.button("💬 Question Generator", key="qa2", use_container_width=True): st.session_state.page="questions"; st.rerun()
        if st.button("🎤 Mock Interview",      key="qa3", use_container_width=True): st.session_state.page="mock";      st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def _process_resume(uploaded_file, role):
    from services.resume_parser import extract_text
    from services.ats_checker   import run as ats_run
    from services.resume_analyzer import run as analyzer_run
    from services.resume_validator import is_valid_resume

    with st.spinner("Analysing your resume..."):
        try:
            suffix = "." + uploaded_file.name.rsplit(".", 1)[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            text = extract_text(tmp_path, uploaded_file.name)
            os.unlink(tmp_path)

            valid, reason = is_valid_resume(text)
            if not valid:
                st.session_state.upload_error = reason
                st.session_state.resume_data  = None
                st.rerun()
                return

            ats      = ats_run(text, role)
            analysis = analyzer_run(text, role,
                                    ats["found_skills"],
                                    ats["missing_skills"],
                                    ats["sections"])

            st.session_state.resume_data = {
                "filename": uploaded_file.name,
                "role":     role,
                "raw_text": text,
                **ats,
                **analysis,
            }
            st.session_state.role = role
            save_resume_to_db()
            st.session_state.page = "ats"
            st.rerun()
        except Exception as e:
            st.session_state.upload_error = f"Error processing resume: {e}"
            st.rerun()
