"""Final interview report page (score breakdown + downloadable summary)."""
import streamlit as st

def page_final_report():
    from services.report_generator import build

    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">Final Interview Report</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">Overall performance in the interview</p>', unsafe_allow_html=True)

    interview = {
        "role":        st.session_state.get("role",""),
        "personalized":st.session_state.get("personalized", False),
        "questions":   st.session_state.get("questions", []),
        "answers":     {str(k): v for k,v in st.session_state.get("answers",{}).items()},
        "evaluations": {str(k): v for k,v in st.session_state.get("evaluations",{}).items()},
    }
    resume = st.session_state.resume_data
    report = build(interview, resume)

    if report.get("attempted", 0) == 0:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:48px">📋</div><div style="color:#3A2E2A;font-size:17px;font-weight:500;margin-top:12px">No interview data yet</div><div style="color:#9C7A6B;margin-top:6px">Complete a mock interview first to generate your report.</div></div>', unsafe_allow_html=True)
        if st.button("Start Mock Interview →", type="primary"):
            st.session_state.page = "questions"; st.rerun()
        return

    os_val = report.get("overall_score", 0)
    lc     = "#10B981" if os_val >= 8 else "#E8896A" if os_val >= 6 else "#F59E0B"
    stars  = report.get("stars","")

    pers_badge  = '<span class="b-cyan" style="font-size:15px">✨ Personalized</span>' if report.get("personalized") else ""
    role_badge  = f'<span class="b-green" style="font-size:15px">{report.get("role","")}</span>' if report.get("role") else ""
    st.markdown(f"""
    <div class="ai-card" style="text-align:center;padding:36px">
      <div style="font-size:60px;font-weight:800;color:{lc};line-height:1">
        {os_val}<span style="font-size:25px;color:#9C7A6B">/10</span></div>
      <div style="color:#F59E0B;font-size:22px;letter-spacing:2px;margin:8px 0">{stars}</div>
      <div style="display:flex;gap:8px;justify-content:center;margin:10px 0">
        <span class="b-accent" style="font-size:15px">{report.get('performance_label','')}</span>
        {pers_badge} {role_badge}
      </div>
      <p style="color:#9C7A6B;font-size:15px;max-width:520px;margin:16px auto 0;line-height:1.9">
        {report.get('summary','')}</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, lbl, val, icon in [
        (c1, "Total Questions", report.get("total_questions",0), "📝"),
        (c2, "Attempted",       report.get("attempted",0),       "✏️"),
        (c3, "Correct (≥6)",    report.get("correct",0),         "✅"),
        (c4, "Accuracy",        f"{report.get('accuracy',0)}%",  "🎯"),
    ]:
        with col:
            st.markdown(f"""
            <div class="ai-card" style="text-align:center">
              <div style="font-size:25px;margin-bottom:6px">{icon}</div>
              <div style="font-size:31px;font-weight:700;color:#3A2E2A">{val}</div>
              <div style="font-size:13.5px;color:#9C7A6B">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:16px">Score Breakdown</div>', unsafe_allow_html=True)
        for lbl, sc in report.get("breakdown",{}).items():
            pc = int(sc/10*100)
            fc = "p-green" if sc >= 7 else "p-yellow" if sc < 5 else ""
            st.markdown(f"""
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:15px;color:#9C7A6B">{lbl}</span>
                <span style="font-size:15px;color:#3A2E2A;font-weight:600">{sc}/10</span>
              </div>
              <div class="prog-bar"><div class="prog-fill {fc}" style="width:{pc}%"></div></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        ats = report.get("ats_score", 0)
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:16px">Resume Performance</div>', unsafe_allow_html=True)
        if ats:
            combined = int(os_val/10*0.6*100 + ats/100*0.4*100)
            ag = "p-green" if ats >= 70 else ""
            ig = int(os_val/10*100)
            st.markdown(f"""
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:15px;color:#9C7A6B">ATS Resume Score</span>
                <span style="font-size:15px;color:#3A2E2A;font-weight:600">{ats}/100</span>
              </div>
              <div class="prog-bar"><div class="prog-fill {ag}" style="width:{ats}%"></div></div>
            </div>
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:15px;color:#9C7A6B">Interview Score</span>
                <span style="font-size:15px;color:#3A2E2A;font-weight:600">{os_val}/10</span>
              </div>
              <div class="prog-bar"><div class="prog-fill" style="width:{ig}%"></div></div>
            </div>
            <div class="ai-card-flat" style="text-align:center">
              <div style="font-size:13.5px;color:#9C7A6B;margin-bottom:4px">Combined Readiness</div>
              <div style="font-size:35px;font-weight:700;color:#E8896A">{combined}%</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:15px">Upload a resume to see combined score.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    qs    = st.session_state.get("questions",[])
    evals = st.session_state.get("evaluations",{})
    if qs:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Q&A Review</div>', unsafe_allow_html=True)
        for i, q in enumerate(qs):
            ev = evals.get(i) or evals.get(str(i))
            if ev:
                es = ev.get("score",0)
                eb = "b-green" if es >= 7 else "b-yellow" if es >= 5 else "b-red"
                fb = ev.get("feedback","")[:100]
                st.markdown(f"""
                <div style="padding:14px 0;border-bottom:1px solid #F0DDD0">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                    <span style="width:26px;height:26px;border-radius:50%;background:rgba(232,137,106,.2);
                                 color:#E8896A;font-size:12.5px;font-weight:700;display:flex;align-items:center;
                                 justify-content:center;flex-shrink:0">{i+1}</span>
                    <span style="font-weight:600;font-size:15px;color:#3A2E2A">{q['question']}</span>
                  </div>
                  <div style="display:flex;gap:8px;align-items:center;padding-left:36px">
                    <span class="{eb}">{es}/10</span>
                    <span style="font-size:13.5px;color:#9C7A6B">{fb}…</span>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid #F0DDD0"><span style="font-size:15px;color:#9C7A6B">{i+1}. {q["question"]}</span> <span class="b-yellow">Not answered</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    lines = [
        "AI INTERVIEW PREP — FINAL REPORT","="*50,
        f"Role          : {report.get('role','-')}",
        f"Overall Score : {os_val}/10  {stars}",
        f"Performance   : {report.get('performance_label','-')}",
        f"ATS Score     : {report.get('ats_score',0)}/100",
        f"Accuracy      : {report.get('accuracy',0)}%","",
        "Score Breakdown:",
    ] + [f"  {k}: {v}/10" for k,v in report.get("breakdown",{}).items()] + \
        ["","Summary:", report.get("summary","")]

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Practice Again", type="primary", use_container_width=True):
            st.session_state.page = "questions"; st.rerun()
    with c2:
        st.download_button("⬇️ Download Report", data="\n".join(lines),
                           file_name="interview_report.txt",
                           mime="text/plain", use_container_width=True)
