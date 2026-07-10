"""ATS resume score breakdown page."""
import streamlit as st

from ui.widgets import svg_ring

def page_ats_checker():
    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">ATS Resume Checker</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">Check how well your resume performs in ATS</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:48px">📄</div><div style="color:#3A2E2A;font-size:17px;font-weight:500;margin-top:12px">No resume uploaded yet</div><div style="color:#9C7A6B;margin-top:6px">Go to Home and upload a PDF or DOCX resume.</div></div>', unsafe_allow_html=True)
        if st.button("← Back to Home"): st.session_state.page="home"; st.rerun()
        return

    pct   = resume.get("ats_score", 0)
    color = "#10B981" if pct >= 70 else "#F59E0B" if pct >= 50 else "#EF4444"
    badge = "b-green" if pct >= 70 else "b-yellow" if pct >= 50 else "b-red"

    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
          {svg_ring(pct, 100, size=110, color=color, sub="/100")}
          <span class="{badge}">{resume.get('score_label','')}</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        missing = resume.get("missing_skills", [])
        hint    = (f'Keywords like <em>{", ".join(missing[:3])}</em> are missing — adding them would push your score higher.'
                   if missing else "Great keyword coverage! Focus on measurable achievements.")
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-weight:600;color:#3A2E2A;margin-bottom:8px">Score Explanation</div>
          <p style="font-size:15px;color:#9C7A6B;line-height:1.8">
            Your resume scores <strong style="color:#3A2E2A">{pct}/100</strong> for ATS compatibility. {hint}
          </p>
        </div>""", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Section Analysis</div>', unsafe_allow_html=True)
        for sec, ok in resume.get("sections",{}).items():
            icon  = "✅" if ok else "❌"
            color_s = "#3A2E2A" if ok else "#9C7A6B"
            st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid #F0DDD0;font-size:15px;color:{color_s}">{icon} {sec}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Missing Keywords</div>', unsafe_allow_html=True)
        miss = resume.get("missing_skills",[])
        if miss:
            for sk in miss:
                st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid #F0DDD0;font-size:15px;color:#9C7A6B"><span style="color:#EF4444">✗</span> {sk}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#10B981;font-size:15px">🎉 All key skills found!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with p3:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Suggestions</div>', unsafe_allow_html=True)
        for tip in resume.get("suggestions",[]):
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:8px;padding:5px 0;border-bottom:1px solid #F0DDD0;font-size:13.5px;color:#3A2E2A"><span style="color:#F59E0B;flex-shrink:0">●</span>{tip}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    found = resume.get("found_skills",[])
    if found:
        tags = "".join(f'<span class="tag">{s}</span>' for s in found)
        st.markdown(f'<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Keywords found in your resume</div>{tags}</div>', unsafe_allow_html=True)
