"""Resume strengths/weaknesses + skill-gap analysis page."""
import streamlit as st

def page_resume_analysis():
    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">Resume Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">AI-powered resume analysis and insights</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:48px">📊</div><div style="color:#3A2E2A;font-size:17px;margin-top:12px">No resume uploaded</div></div>', unsafe_allow_html=True)
        if st.button("← Back to Home"): st.session_state.page="home"; st.rerun()
        return

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#10B981;font-weight:600;text-transform:uppercase;margin-bottom:12px">✅ Strengths</div>', unsafe_allow_html=True)
        for s in resume.get("strengths",[]):
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:15px;color:#3A2E2A"><span style="color:#10B981">✓</span>{s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#EF4444;font-weight:600;text-transform:uppercase;margin-bottom:12px">⚠️ Weaknesses</div>', unsafe_allow_html=True)
        for w in resume.get("weaknesses",[]):
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:15px;color:#3A2E2A"><span style="color:#EF4444">✗</span>{w}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if resume.get("top_skills"):
        chips = "".join(f'<span class="tag">⌨ {s}</span>' for s in resume["top_skills"])
        st.markdown(f'<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Top Skills Found</div>{chips}</div>', unsafe_allow_html=True)

    score_10 = round(resume.get("ats_score",0) / 10, 1)
    st.markdown(f"""
    <div class="ai-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
        <div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase">Resume Summary</div>
        <span class="b-accent">Overall Score: {score_10}/10</span>
      </div>
      <p style="font-size:15px;color:#3A2E2A;line-height:1.8">{resume.get('summary','')}</p>
    </div>""", unsafe_allow_html=True)

    try:
        from services.skill_gap_analyzer import analyse
        gap  = analyse(resume["role"], resume.get("found_skills",[]), resume.get("missing_skills",[]))
        pct  = gap["coverage_percent"]
        bc   = "b-green" if pct >= 70 else "b-yellow"
        pfil = "p-green" if pct >= 70 else "p-yellow"
        st.markdown(f"""
        <div class="ai-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase">Skill Gap — {resume['role']}</div>
            <span class="{bc}">{pct}% coverage</span>
          </div>
          <div class="prog-bar"><div class="prog-fill {pfil}" style="width:{pct}%"></div></div>
        </div>""", unsafe_allow_html=True)
        if gap.get("gaps"):
            for g in gap["gaps"]:
                ga, gb = st.columns([4,1])
                with ga:
                    pb = "b-red" if g["priority"]=="High" else "b-yellow"
                    st.markdown(f'<span class="{pb}">{g["priority"]}</span> <span style="color:#3A2E2A;font-size:15px;font-weight:500"> {g["skill"]}</span>', unsafe_allow_html=True)
                with gb:
                    st.markdown(f'<a href="{g["resource"]}" target="_blank" style="color:#E8896A;font-size:13.5px">Learn →</a>', unsafe_allow_html=True)
    except Exception:
        pass

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 Generate Questions", type="primary", use_container_width=True):
            st.session_state.page = "questions"; st.rerun()
    with c2:
        if st.button("⬆️ Re-upload Resume", use_container_width=True):
            st.session_state.page = "home"; st.rerun()
