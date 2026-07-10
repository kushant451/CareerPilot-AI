"""Career-readiness dashboard aggregating all modules."""
import streamlit as st

from ui.widgets import avg_score

def page_career_dashboard():
    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">Career Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">Your career-readiness snapshot, all in one place</p>', unsafe_allow_html=True)

    resume   = st.session_state.resume_data
    ats      = resume.get("ats_score", 0) if resume else 0
    mock_avg = avg_score()
    career   = st.session_state.career_recommendations
    roadmap  = st.session_state.roadmap_data
    jobmatch = st.session_state.job_match_result

    top_path   = career["top_matches"][0] if career and career.get("top_matches") else None
    top_pct    = top_path["match_percent"] if top_path else 0
    weeks_left = roadmap["weeks"] if roadmap else 0
    jm_pct     = jobmatch["match_percent"] if jobmatch else 0

    readiness = round((ats * 0.25 + mock_avg * 10 * 0.35 + top_pct * 0.2 + jm_pct * 0.2))

    st.markdown(f"""
    <div class="ai-card" style="text-align:center;padding:36px">
      <div style="font-size:13.5px;color:#9C7A6B;font-weight:600;text-transform:uppercase;letter-spacing:.5px">Overall Career Readiness</div>
      <div style="font-size:56px;font-weight:800;color:#E8896A;line-height:1;margin-top:8px">{readiness}%</div>
      <p style="color:#9C7A6B;font-size:15px;max-width:520px;margin:12px auto 0;line-height:1.8">
        Combines your ATS resume score, mock interview performance, best career-path match, and latest job-description match.</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        color = "#10B981" if ats >= 70 else "#F59E0B" if ats >= 50 else "#EF4444"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:12.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">📄 ATS Score</div>
          <div style="font-size:29px;font-weight:700;color:{color}">{ats}<span style="font-size:13.5px;color:#9C7A6B">/100</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_ats", use_container_width=True): st.session_state.page="ats"; st.rerun()

    with c2:
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:12.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">🎤 Mock Interview</div>
          <div style="font-size:29px;font-weight:700;color:#E8896A">{mock_avg}<span style="font-size:13.5px;color:#9C7A6B">/10</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_mock", use_container_width=True): st.session_state.page="report"; st.rerun()

    with c3:
        label = top_path["title"] if top_path else "Not analysed"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:12.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">🧭 Best Career Fit</div>
          <div style="font-size:18px;font-weight:700;color:#3A2E2A;margin-bottom:4px">{label}</div>
          <div style="font-size:15px;color:#10B981;font-weight:600">{top_pct}% match</div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_career", use_container_width=True): st.session_state.page="career"; st.rerun()

    with c4:
        label = f"{jm_pct}% match" if jobmatch else "Not analysed"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:12.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">🎯 Latest Job Match</div>
          <div style="font-size:29px;font-weight:700;color:#E8896A">{label}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_jm", use_container_width=True): st.session_state.page="jobmatch"; st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">🗺️ Learning Roadmap Progress</div>', unsafe_allow_html=True)
        if roadmap:
            st.markdown(f"""
            <p style="font-size:15px;color:#3A2E2A;line-height:1.8">
              Your <strong>{weeks_left}-week</strong> roadmap for <strong>{roadmap['role']}</strong> covers
              <strong style="color:#E8896A">{roadmap['total_skills']}</strong> skills across
              {len(roadmap.get('milestones', []))} milestones.</p>""", unsafe_allow_html=True)
            if st.button("Open Roadmap →", key="d_roadmap_open"):
                st.session_state.page = "roadmap"; st.rerun()
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:15px">No roadmap generated yet.</p>', unsafe_allow_html=True)
            if st.button("Generate Roadmap →", key="d_roadmap_gen"):
                st.session_state.page = "roadmap"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">🧭 Top 3 Career Matches</div>', unsafe_allow_html=True)
        if career and career.get("top_matches"):
            for p in career["top_matches"][:3]:
                pc = p["match_percent"]
                fc = "p-green" if pc >= 70 else "p-yellow" if pc >= 40 else ""
                st.markdown(f"""
                <div style="margin-bottom:12px">
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="font-size:15px;color:#3A2E2A">{p['title']}</span>
                    <span style="font-size:15px;color:#9C7A6B;font-weight:600">{pc}%</span>
                  </div>
                  <div class="prog-bar"><div class="prog-fill {fc}" style="width:{pc}%"></div></div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:15px">No career recommendations yet.</p>', unsafe_allow_html=True)
            if st.button("Get Recommendations →", key="d_career_gen"):
                st.session_state.page = "career"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
