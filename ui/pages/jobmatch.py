"""Job description match analyzer page."""
import streamlit as st

from ui.widgets import svg_ring
from ui.db_helpers import save_job_match_to_db

def page_job_match_analyzer():
    from config.settings import ROLES
    from services.job_match_analyzer import analyze

    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">Job Match Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">Paste a job description to see how well your resume matches</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:48px">🎯</div><div style="color:#3A2E2A;font-size:17px;font-weight:500;margin-top:12px">No resume uploaded yet</div><div style="color:#9C7A6B;margin-top:6px">Go to Home and upload a PDF or DOCX resume first.</div></div>', unsafe_allow_html=True)
        if st.button("← Back to Home"): st.session_state.page="home"; st.rerun()
        return

    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    role = st.selectbox("Role this job description is for", ROLES, key="jm_role",
                        index=ROLES.index(resume.get("role")) if resume.get("role") in ROLES else 0)
    jd = st.text_area("Paste the job description here", height=200, key="jm_jd",
                      value=st.session_state.job_description,
                      placeholder="Paste the full job description text...")
    if st.button("🎯 Analyze Match", type="primary", use_container_width=True):
        if jd.strip():
            st.session_state.job_description = jd
            with st.spinner("Comparing your resume against the job description..."):
                result = analyze(resume.get("raw_text", ""), jd, role)
                st.session_state.job_match_result = result
                save_job_match_to_db(role, jd, result)
            st.rerun()
        else:
            st.warning("Please paste a job description first.")
    st.markdown('</div>', unsafe_allow_html=True)

    result = st.session_state.job_match_result
    if not result:
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:39px">🎯</div><div style="color:#9C7A6B;margin-top:12px">Paste a job description above and click "Analyze Match".</div></div>', unsafe_allow_html=True)
        return

    pct = result["match_percent"]
    color = "#10B981" if pct >= 75 else "#E8896A" if pct >= 50 else "#F59E0B" if pct >= 25 else "#EF4444"

    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
          {svg_ring(pct, 100, size=110, color=color, sub="/100")}
          <span class="{result['badge']}">{result['label']}</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-weight:600;color:#3A2E2A;margin-bottom:8px">Fit Summary</div>
          <p style="font-size:15px;color:#3A2E2A;line-height:1.8">{result['summary']}</p>
        </div>""", unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#10B981;font-weight:600;text-transform:uppercase;margin-bottom:12px">✅ Matched Keywords</div>', unsafe_allow_html=True)
        if result["matched_keywords"]:
            tags = "".join(f'<span class="tag">{s}</span>' for s in result["matched_keywords"])
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:15px">No overlapping keywords found.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with p2:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#EF4444;font-weight:600;text-transform:uppercase;margin-bottom:12px">❌ Missing Keywords</div>', unsafe_allow_html=True)
        if result["missing_keywords"]:
            tags = "".join(f'<span class="tag" style="background:rgba(239,68,68,.12);color:#EF4444;border-color:rgba(239,68,68,.2)">{s}</span>' for s in result["missing_keywords"])
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#10B981;font-size:15px">🎉 No missing keywords!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
