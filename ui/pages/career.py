"""AI career-path recommendation page."""
import streamlit as st

from ui.db_helpers import save_career_rec_to_db

def page_career_recommendation():
    from services.career_recommender import recommend

    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">AI Career Recommendation</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">Discover the career paths that best fit your current skills</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:48px">🧭</div><div style="color:#3A2E2A;font-size:17px;font-weight:500;margin-top:12px">No resume uploaded yet</div><div style="color:#9C7A6B;margin-top:6px">Go to Home and upload a PDF or DOCX resume to get personalised recommendations.</div></div>', unsafe_allow_html=True)
        if st.button("← Back to Home"): st.session_state.page="home"; st.rerun()
        return

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-top:6px">Uses the skills detected in your resume to rank the career paths you are best suited for right now.</p>', unsafe_allow_html=True)
    with c2:
        if st.button("🧭 Get Recommendations", type="primary", use_container_width=True):
            with st.spinner("Analysing your skill profile..."):
                result = recommend(resume.get("role", st.session_state.role),
                                    resume.get("found_skills", []),
                                    resume.get("top_skills", []))
                st.session_state.career_recommendations = result
                save_career_rec_to_db(result)
            st.rerun()

    result = st.session_state.career_recommendations
    if not result:
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:39px">🧭</div><div style="color:#9C7A6B;margin-top:12px">Click "Get Recommendations" to see your best-fit career paths.</div></div>', unsafe_allow_html=True)
        return

    matches = result.get("top_matches", [])
    if not matches:
        st.info(result.get("insight", "No recommendations available."))
        return

    st.markdown(f"""
    <div class="ai-card" style="background:rgba(232,137,106,.08)">
      <div style="font-size:13.5px;color:#E8896A;font-weight:600;text-transform:uppercase;margin-bottom:8px">✨ AI Insight</div>
      <p style="font-size:15.5px;color:#3A2E2A;line-height:1.8">{result.get('insight','')}</p>
    </div>""", unsafe_allow_html=True)

    for i, path in enumerate(matches):
        pct   = path["match_percent"]
        color = "#10B981" if pct >= 70 else "#E8896A" if pct >= 40 else "#F59E0B"
        badge = "b-green" if pct >= 70 else "b-accent" if pct >= 40 else "b-yellow"
        matched_tags = "".join(f'<span class="tag">✓ {s}</span>' for s in path["matched_skills"]) or '<span style="color:#9C7A6B;font-size:13.5px">None yet</span>'
        missing_tags = "".join(f'<span class="tag" style="background:rgba(239,68,68,.12);color:#EF4444;border-color:rgba(239,68,68,.2)">{s}</span>' for s in path["missing_skills"]) or '<span style="color:#10B981;font-size:13.5px">All core skills covered 🎉</span>'
        top_flag = ' <span class="b-green">🏆 Best Match</span>' if i == 0 else ""
        st.markdown(f"""
        <div class="ai-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:6px">
            <div>
              <span style="font-size:19px;font-weight:700;color:#3A2E2A">{path['title']}</span>{top_flag}
              <div style="color:#9C7A6B;font-size:14px;margin-top:4px">{path['description']}</div>
            </div>
            <div style="text-align:center;flex-shrink:0">
              <div style="font-size:27px;font-weight:800;color:{color}">{pct}%</div>
              <span class="{badge}" style="font-size:12px">match</span>
            </div>
          </div>
          <div class="prog-bar" style="margin:10px 0"><div class="prog-fill" style="width:{pct}%;background:{color}"></div></div>
          <div style="display:flex;gap:14px;margin-top:10px;flex-wrap:wrap">
            <span class="b-accent" style="font-size:12.5px">Growth: {path.get('growth_outlook','—')}</span>
          </div>
          <div style="margin-top:12px">
            <div style="font-size:12.5px;color:#9C7A6B;font-weight:600;text-transform:uppercase;margin-bottom:6px">Skills you have</div>
            {matched_tags}
          </div>
          <div style="margin-top:10px">
            <div style="font-size:12.5px;color:#9C7A6B;font-weight:600;text-transform:uppercase;margin-bottom:6px">Skills to build</div>
            {missing_tags}
          </div>
        </div>""", unsafe_allow_html=True)

    if st.button("🗺️ Build a Learning Roadmap for My Top Match", type="primary", use_container_width=True):
        st.session_state.page = "roadmap"; st.rerun()
