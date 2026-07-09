import streamlit as st
import uuid, os, time, tempfile

st.set_page_config(
    page_title="AI Interview Prep",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    st.markdown("""
<style>
#MainMenu, footer, header {display:none !important}
.block-container {padding:1.5rem 2rem !important; max-width:1100px}
.stApp {background:#FFF6F0}
section[data-testid="stSidebar"] {background:#FFFFFF; border-right:1px solid #F0DDD0; box-shadow:2px 0 12px rgba(232,137,106,.06)}

.ai-card {background:#FFFFFF; border:1px solid #F3E1D3; border-radius:16px; padding:20px; margin-bottom:16px; box-shadow:0 2px 10px rgba(232,137,106,.08)}
.ai-card-flat {background:#FDEAE0; border:1px solid #F3E1D3; border-radius:12px; padding:16px; margin-bottom:12px}

.b-green  {background:rgba(16,185,129,.12);  color:#10B981; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:500; display:inline-block}
.b-red    {background:rgba(239,68,68,.12);   color:#EF4444; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:500; display:inline-block}
.b-yellow {background:rgba(245,158,11,.12);  color:#F59E0B; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:500; display:inline-block}
.b-accent {background:rgba(232,137,106,.15);  color:#E8896A; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:500; display:inline-block}
.b-cyan   {background:rgba(6,182,212,.12);   color:#06B6D4; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:500; display:inline-block}

.tag {display:inline-block; background:rgba(232,137,106,.15); color:#E8896A; padding:4px 12px;
      border-radius:999px; font-size:12px; margin:3px; border:1px solid rgba(232,137,106,.2)}

.prog-bar    {height:6px; border-radius:3px; background:#FDEAE0; overflow:hidden; margin:4px 0}
.prog-fill   {height:100%; border-radius:3px; background:#E8896A}
.p-green     {background:#10B981}
.p-yellow    {background:#F59E0B}
.p-red       {background:#EF4444}

.waveform {display:flex; align-items:center; gap:3px; height:32px; margin:10px 0}
.waveform span {width:3px; border-radius:2px; background:#E8896A; animation:wv 1.2s ease-in-out infinite}
.waveform span:nth-child(2){animation-delay:.1s} .waveform span:nth-child(3){animation-delay:.2s}
.waveform span:nth-child(4){animation-delay:.3s} .waveform span:nth-child(5){animation-delay:.4s}
.waveform span:nth-child(6){animation-delay:.5s} .waveform span:nth-child(7){animation-delay:.6s}
.waveform span:nth-child(8){animation-delay:.7s} .waveform span:nth-child(9){animation-delay:.3s}
.waveform span:nth-child(10){animation-delay:.15s} .waveform span:nth-child(11){animation-delay:.55s}
.waveform span:nth-child(12){animation-delay:.25s}
@keyframes wv {0%,100%{height:10%} 50%{height:100%}}

.stButton>button {
    border:none !important; border-radius:8px !important; font-weight:500 !important
}
button[kind="primary"], button[kind="primaryFormSubmit"] {
    background:#E8896A !important; color:#fff !important;
}
button[kind="primary"]:hover {background:#F0A184 !important}
button[kind="secondary"] {
    background:transparent !important; color:#6B5248 !important;
    text-align:left !important; justify-content:flex-start !important;
    padding-left:14px !important; font-weight:500 !important;
}
button[kind="secondary"]:hover {background:#FDEAE0 !important; color:#3A2E2A !important}
section[data-testid="stSidebar"] button[kind="primary"] {
    box-shadow:0 2px 8px rgba(232,137,106,.35) !important;
}
.stTextArea>div>textarea {
    background:#FDEAE0 !important; border:1px solid #E8C7AE !important;
    color:#3A2E2A !important; border-radius:8px !important
}
.stSelectbox>div>div {
    background:#FDEAE0 !important; border:1px solid #E8C7AE !important; color:#3A2E2A !important
}
.stFileUploader>div {background:#FDEAE0 !important; border:1px solid #E8C7AE !important; border-radius:8px !important}
label {color:#9C7A6B !important; font-size:12px !important}
.stDownloadButton>button {
    background:#FDEAE0 !important; border:1px solid #E8C7AE !important;
    color:#3A2E2A !important; border-radius:8px !important
}
.stAlert {border-radius:8px !important}
div[data-testid="stDecoration"] {display:none}
.stDeployButton {display:none}
[data-testid="stMarkdownContainer"]:empty {display:none !important}
[data-testid="element-container"]:empty {display:none !important}
.ai-card:empty {display:none !important}
</style>
""", unsafe_allow_html=True)


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


def render_sidebar():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;padding:8px 0 20px;
                border-bottom:1px solid #F0DDD0;margin-bottom:12px'>
      <div style='width:60px;height:60px;border-radius:15px;background:#E8896A;
                  display:flex;align-items:center;justify-content:center;font-size:28px'>🤖</div>
      <div>
        <div style='font-size:24px;font-weight:900;color:#3A2E2A'>AI Interview</div>
        <div style='font-size:16px;color:#9C7A6B'>Preparation Assistant</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    nav = [
        ("home",       "🏠", "Home"),
        ("ats",        "📄", "ATS Checker"),
        ("analysis",   "📊", "Resume Analysis"),
        ("career",     "🧭", "Career Recommendation"),
        ("roadmap",    "🗺️", "Learning Roadmap"),
        ("jobmatch",   "🎯", "Job Match Analyzer"),
        ("questions",  "💬", "Question Generator"),
        ("mock",       "🎤", "Mock Interview"),
        ("report",     "📋", "Final Report"),
        ("dashboard",  "📈", "Career Dashboard"),
    ]
    for key, icon, label in nav:
        active = st.session_state.page == key
        btn_type = "primary" if active else "secondary"
        if st.button(f"{icon}  {label}", key=f"nav_{key}",
                     use_container_width=True, type=btn_type):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='background:rgba(232,137,106,.1);border:1px solid #E8C7AE;
                border-radius:12px;padding:14px'>
      <div style='font-size:11px;color:#F59E0B;font-weight:600;margin-bottom:4px'>⭐ Pro Features</div>
      <div style='font-size:11.5px;color:#9C7A6B;margin-bottom:10px'>
        Unlimited mock interviews, AI feedback & analytics.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  New Session", use_container_width=True, key="nav_reset"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


def svg_ring(value, max_val, size=100, color="#E8896A", sub=""):
    pct   = (value / max_val) if max_val else 0
    r     = size * 0.42
    circ  = 2 * 3.14159 * r
    dash  = pct * circ
    cx = cy = size / 2
    fs = size * 0.22
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#F0DDD0" stroke-width="{size*.08}"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}"
              stroke-width="{size*.08}" stroke-dasharray="{dash:.1f} {circ:.1f}"
              stroke-linecap="round" transform="rotate(-90 {cx} {cy})"/>
      <text x="{cx}" y="{cy-.04*size}" text-anchor="middle" dominant-baseline="central"
            fill="{color}" font-size="{fs}" font-weight="700"
            font-family="Segoe UI,sans-serif">{value}</text>
      <text x="{cx}" y="{cy+size*.2}" text-anchor="middle" fill="#9C7A6B"
            font-size="{size*.1}" font-family="Segoe UI,sans-serif">{sub}</text>
    </svg>"""


def avg_score():
    evals  = st.session_state.get("evaluations", {})
    scores = [v["score"] for v in evals.values()
              if isinstance(v, dict) and "score" in v]
    return round(sum(scores) / len(scores), 1) if scores else 0.0

def diff_badge(difficulty):
    cls = {"Easy":"b-green","Medium":"b-yellow","Hard":"b-red"}.get(difficulty,"b-accent")
    return f'<span class="{cls}">{difficulty}</span>'

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


def page_home():
    from config.settings import ROLES

    st.markdown("""
    <div style="text-align:center; padding:18px 0 32px">
        <div style="font-size:44px; margin-bottom:6px">👋</div>
        <h1 style="color:#3A2E2A; font-size:34px; font-weight:800; margin:0 0 8px">Welcome back</h1>
        <p style="color:#9C7A6B; font-size:17px; margin:0">Let's crack your dream job!</p>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.upload_error:
        st.error(st.session_state.upload_error)
        st.session_state.upload_error = None

    col_form, col_ring = st.columns([3, 1])
    with col_form:
        st.markdown('<div class="ai-card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:25px;font-weight:700;color:#3A2E2A;margin-bottom:6px">🎯 Your AI Interview Coach</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#9C7A6B;font-size:18px;margin-bottom:16px">Upload your resume, check ATS score, practice interviews and improve your skills.</p>', unsafe_allow_html=True)

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
        <div class="ai-card-flat" style="text-align:center">
          <div style="font-size:10px;color:#9C7A6B;font-weight:600;text-transform:uppercase;
                      letter-spacing:.4px;margin-bottom:10px">Overall Progress</div>
          {svg_ring(pct, 100, size=90, color="#E8896A", sub="%")}
          <div style="margin-top:10px;display:flex;flex-direction:column;gap:5px">
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#9C7A6B">
              <span>● ATS</span>
              <span style="color:#3A2E2A;font-weight:600">{ats}/100</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#9C7A6B">
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
          <div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;
                      letter-spacing:.4px;margin-bottom:6px">ATS Score</div>
          <div style="font-size:28px;font-weight:700;color:{color};margin-bottom:8px">
            {ats_score}<span style="font-size:13px;color:#9C7A6B">/100</span></div>
          <span class="{badge}">{slabel}</span>
        </div>""", unsafe_allow_html=True)
        if has_resume and st.button("View ATS Details →", key="h_ats"):
            st.session_state.page = "ats"; st.rerun()

    with c2:
        badge2 = "b-green" if st.session_state.interview_started else "b-yellow"
        label2 = "Completed" if st.session_state.interview_started else "Not started"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;
                      letter-spacing:.4px;margin-bottom:6px">Mock Score</div>
          <div style="font-size:28px;font-weight:700;color:#E8896A;margin-bottom:8px">
            {int_score}<span style="font-size:13px;color:#9C7A6B">/10</span></div>
          <span class="{badge2}">{label2}</span>
        </div>""", unsafe_allow_html=True)
        if st.session_state.interview_started:
            if st.button("View Report →", key="h_rep"):
                st.session_state.page = "report"; st.rerun()
        else:
            if st.button("Start Now →", key="h_start"):
                st.session_state.page = "questions"; st.rerun()

    with c3:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;letter-spacing:.4px;margin-bottom:12px">Quick Actions</div>', unsafe_allow_html=True)
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


def page_ats_checker():
    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">ATS Resume Checker</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">Check how well your resume performs in ATS</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:44px">📄</div><div style="color:#3A2E2A;font-size:15px;font-weight:500;margin-top:12px">No resume uploaded yet</div><div style="color:#9C7A6B;margin-top:6px">Go to Home and upload a PDF or DOCX resume.</div></div>', unsafe_allow_html=True)
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
          <p style="font-size:13px;color:#9C7A6B;line-height:1.8">
            Your resume scores <strong style="color:#3A2E2A">{pct}/100</strong> for ATS compatibility. {hint}
          </p>
        </div>""", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Section Analysis</div>', unsafe_allow_html=True)
        for sec, ok in resume.get("sections",{}).items():
            icon  = "✅" if ok else "❌"
            color_s = "#3A2E2A" if ok else "#9C7A6B"
            st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid #F0DDD0;font-size:13px;color:{color_s}">{icon} {sec}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Missing Keywords</div>', unsafe_allow_html=True)
        miss = resume.get("missing_skills",[])
        if miss:
            for sk in miss:
                st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid #F0DDD0;font-size:13px;color:#9C7A6B"><span style="color:#EF4444">✗</span> {sk}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#10B981;font-size:13px">🎉 All key skills found!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with p3:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Suggestions</div>', unsafe_allow_html=True)
        for tip in resume.get("suggestions",[]):
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:8px;padding:5px 0;border-bottom:1px solid #F0DDD0;font-size:12px;color:#3A2E2A"><span style="color:#F59E0B;flex-shrink:0">●</span>{tip}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    found = resume.get("found_skills",[])
    if found:
        tags = "".join(f'<span class="tag">{s}</span>' for s in found)
        st.markdown(f'<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Keywords found in your resume</div>{tags}</div>', unsafe_allow_html=True)


def page_resume_analysis():
    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">Resume Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">AI-powered resume analysis and insights</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:44px">📊</div><div style="color:#3A2E2A;font-size:15px;margin-top:12px">No resume uploaded</div></div>', unsafe_allow_html=True)
        if st.button("← Back to Home"): st.session_state.page="home"; st.rerun()
        return

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#10B981;font-weight:600;text-transform:uppercase;margin-bottom:12px">✅ Strengths</div>', unsafe_allow_html=True)
        for s in resume.get("strengths",[]):
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:13px;color:#3A2E2A"><span style="color:#10B981">✓</span>{s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#EF4444;font-weight:600;text-transform:uppercase;margin-bottom:12px">⚠️ Weaknesses</div>', unsafe_allow_html=True)
        for w in resume.get("weaknesses",[]):
            st.markdown(f'<div style="display:flex;align-items:flex-start;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:13px;color:#3A2E2A"><span style="color:#EF4444">✗</span>{w}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if resume.get("top_skills"):
        chips = "".join(f'<span class="tag">⌨ {s}</span>' for s in resume["top_skills"])
        st.markdown(f'<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Top Skills Found</div>{chips}</div>', unsafe_allow_html=True)

    score_10 = round(resume.get("ats_score",0) / 10, 1)
    st.markdown(f"""
    <div class="ai-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
        <div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase">Resume Summary</div>
        <span class="b-accent">Overall Score: {score_10}/10</span>
      </div>
      <p style="font-size:13px;color:#3A2E2A;line-height:1.8">{resume.get('summary','')}</p>
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
            <div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase">Skill Gap — {resume['role']}</div>
            <span class="{bc}">{pct}% coverage</span>
          </div>
          <div class="prog-bar"><div class="prog-fill {pfil}" style="width:{pct}%"></div></div>
        </div>""", unsafe_allow_html=True)
        if gap.get("gaps"):
            for g in gap["gaps"]:
                ga, gb = st.columns([4,1])
                with ga:
                    pb = "b-red" if g["priority"]=="High" else "b-yellow"
                    st.markdown(f'<span class="{pb}">{g["priority"]}</span> <span style="color:#3A2E2A;font-size:13px;font-weight:500"> {g["skill"]}</span>', unsafe_allow_html=True)
                with gb:
                    st.markdown(f'<a href="{g["resource"]}" target="_blank" style="color:#E8896A;font-size:12px">Learn →</a>', unsafe_allow_html=True)
    except Exception:
        pass

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 Generate Questions", type="primary", use_container_width=True):
            st.session_state.page = "questions"; st.rerun()
    with c2:
        if st.button("⬆️ Re-upload Resume", use_container_width=True):
            st.session_state.page = "home"; st.rerun()


def page_career_recommendation():
    from services.career_recommender import recommend

    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">AI Career Recommendation</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">Discover the career paths that best fit your current skills</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:44px">🧭</div><div style="color:#3A2E2A;font-size:15px;font-weight:500;margin-top:12px">No resume uploaded yet</div><div style="color:#9C7A6B;margin-top:6px">Go to Home and upload a PDF or DOCX resume to get personalised recommendations.</div></div>', unsafe_allow_html=True)
        if st.button("← Back to Home"): st.session_state.page="home"; st.rerun()
        return

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-top:6px">Uses the skills detected in your resume to rank the career paths you are best suited for right now.</p>', unsafe_allow_html=True)
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
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:36px">🧭</div><div style="color:#9C7A6B;margin-top:12px">Click "Get Recommendations" to see your best-fit career paths.</div></div>', unsafe_allow_html=True)
        return

    matches = result.get("top_matches", [])
    if not matches:
        st.info(result.get("insight", "No recommendations available."))
        return

    st.markdown(f"""
    <div class="ai-card" style="background:rgba(232,137,106,.08)">
      <div style="font-size:12px;color:#E8896A;font-weight:600;text-transform:uppercase;margin-bottom:8px">✨ AI Insight</div>
      <p style="font-size:13.5px;color:#3A2E2A;line-height:1.8">{result.get('insight','')}</p>
    </div>""", unsafe_allow_html=True)

    for i, path in enumerate(matches):
        pct   = path["match_percent"]
        color = "#10B981" if pct >= 70 else "#E8896A" if pct >= 40 else "#F59E0B"
        badge = "b-green" if pct >= 70 else "b-accent" if pct >= 40 else "b-yellow"
        matched_tags = "".join(f'<span class="tag">✓ {s}</span>' for s in path["matched_skills"]) or '<span style="color:#9C7A6B;font-size:12px">None yet</span>'
        missing_tags = "".join(f'<span class="tag" style="background:rgba(239,68,68,.12);color:#EF4444;border-color:rgba(239,68,68,.2)">{s}</span>' for s in path["missing_skills"]) or '<span style="color:#10B981;font-size:12px">All core skills covered 🎉</span>'
        top_flag = ' <span class="b-green">🏆 Best Match</span>' if i == 0 else ""
        st.markdown(f"""
        <div class="ai-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:6px">
            <div>
              <span style="font-size:17px;font-weight:700;color:#3A2E2A">{path['title']}</span>{top_flag}
              <div style="color:#9C7A6B;font-size:12.5px;margin-top:4px">{path['description']}</div>
            </div>
            <div style="text-align:center;flex-shrink:0">
              <div style="font-size:24px;font-weight:800;color:{color}">{pct}%</div>
              <span class="{badge}" style="font-size:10.5px">match</span>
            </div>
          </div>
          <div class="prog-bar" style="margin:10px 0"><div class="prog-fill" style="width:{pct}%;background:{color}"></div></div>
          <div style="display:flex;gap:14px;margin-top:10px;flex-wrap:wrap">
            <span class="b-accent" style="font-size:11px">Growth: {path.get('growth_outlook','—')}</span>
          </div>
          <div style="margin-top:12px">
            <div style="font-size:11px;color:#9C7A6B;font-weight:600;text-transform:uppercase;margin-bottom:6px">Skills you have</div>
            {matched_tags}
          </div>
          <div style="margin-top:10px">
            <div style="font-size:11px;color:#9C7A6B;font-weight:600;text-transform:uppercase;margin-bottom:6px">Skills to build</div>
            {missing_tags}
          </div>
        </div>""", unsafe_allow_html=True)

    if st.button("🗺️ Build a Learning Roadmap for My Top Match", type="primary", use_container_width=True):
        st.session_state.page = "roadmap"; st.rerun()


def page_learning_roadmap():
    from config.settings import ROLES
    from services.roadmap_generator import generate

    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">Learning Roadmap</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">A week-by-week plan to close your skill gaps</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    default_role = resume.get("role") if resume else st.session_state.role
    default_missing = resume.get("missing_skills", []) if resume else []

    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        role = st.selectbox("Target role", ROLES, key="rm_role",
                             index=ROLES.index(default_role) if default_role in ROLES else 0)
    with c2:
        weeks = st.slider("Roadmap length (weeks)", 2, 16, 8, key="rm_weeks")

    if default_missing:
        st.caption(f"Using {len(default_missing)} missing skill(s) detected from your resume for the **{role}** role.")
    else:
        st.caption("No resume on file — the roadmap will use the core skill list for this role instead.")

    if st.button("🗺️ Generate Roadmap", type="primary", use_container_width=True):
        with st.spinner("Building your personalised roadmap..."):
            result = generate(role, default_missing, weeks)
            st.session_state.roadmap_data = result
            save_roadmap_to_db(result)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    result = st.session_state.roadmap_data
    if not result:
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:36px">🗺️</div><div style="color:#9C7A6B;margin-top:12px">Click "Generate Roadmap" to build your learning plan.</div></div>', unsafe_allow_html=True)
        return

    ai_tag = '<span class="b-cyan">✨ AI Generated</span>' if result.get("generated_by_ai") else '<span class="b-accent">Curated Plan</span>'
    st.markdown(f"""
    <div style="display:flex;gap:10px;align-items:center;margin:14px 0">
      <span class="b-green">{result['weeks']} Weeks</span>
      <span class="b-accent">{result['total_skills']} Skills</span>
      {ai_tag}
    </div>""", unsafe_allow_html=True)

    for m in result.get("milestones", []):
        skills_tags = "".join(f'<span class="tag">{s}</span>' for s in m.get("skills", [])) or '<span style="color:#9C7A6B;font-size:12px">Review & practice</span>'
        tasks_html = "".join(f'<div style="padding:4px 0;font-size:12.5px;color:#3A2E2A">☐ {t}</div>' for t in m.get("tasks", []))
        res_html = "".join(f'<a href="{r["url"]}" target="_blank" style="color:#E8896A;font-size:11.5px;margin-right:10px">🔗 {r["skill"]}</a>' for r in m.get("resources", []))
        st.markdown(f"""
        <div class="ai-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <span style="width:30px;height:30px;border-radius:50%;background:rgba(232,137,106,.2);
                         color:#E8896A;font-size:12px;font-weight:700;display:flex;align-items:center;
                         justify-content:center;flex-shrink:0">{m.get('week','?')}</span>
            <span style="font-weight:700;font-size:14.5px;color:#3A2E2A">{m.get('title','')}</span>
          </div>
          <div style="margin-bottom:10px">{skills_tags}</div>
          {tasks_html}
          <div style="margin-top:10px">{res_html}</div>
        </div>""", unsafe_allow_html=True)

    lines = [f"LEARNING ROADMAP — {result['role']} ({result['weeks']} weeks)", "=" * 50, ""]
    for m in result.get("milestones", []):
        lines.append(f"Week {m.get('week')}: {m.get('title')}")
        for t in m.get("tasks", []):
            lines.append(f"  - {t}")
        lines.append("")
    st.download_button("⬇️ Download Roadmap", data="\n".join(lines),
                       file_name="learning_roadmap.txt", mime="text/plain", use_container_width=True)


def page_job_match_analyzer():
    from config.settings import ROLES
    from services.job_match_analyzer import analyze

    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">Job Match Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">Paste a job description to see how well your resume matches</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data
    if not resume:
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:44px">🎯</div><div style="color:#3A2E2A;font-size:15px;font-weight:500;margin-top:12px">No resume uploaded yet</div><div style="color:#9C7A6B;margin-top:6px">Go to Home and upload a PDF or DOCX resume first.</div></div>', unsafe_allow_html=True)
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
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:36px">🎯</div><div style="color:#9C7A6B;margin-top:12px">Paste a job description above and click "Analyze Match".</div></div>', unsafe_allow_html=True)
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
          <p style="font-size:13px;color:#3A2E2A;line-height:1.8">{result['summary']}</p>
        </div>""", unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#10B981;font-weight:600;text-transform:uppercase;margin-bottom:12px">✅ Matched Keywords</div>', unsafe_allow_html=True)
        if result["matched_keywords"]:
            tags = "".join(f'<span class="tag">{s}</span>' for s in result["matched_keywords"])
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:13px">No overlapping keywords found.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with p2:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#EF4444;font-weight:600;text-transform:uppercase;margin-bottom:12px">❌ Missing Keywords</div>', unsafe_allow_html=True)
        if result["missing_keywords"]:
            tags = "".join(f'<span class="tag" style="background:rgba(239,68,68,.12);color:#EF4444;border-color:rgba(239,68,68,.2)">{s}</span>' for s in result["missing_keywords"])
            st.markdown(tags, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#10B981;font-size:13px">🎉 No missing keywords!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def page_question_generator():
    from config.settings import ROLES, DIFFICULTY_LEVELS
    from services.question_generator import generate_generic, generate_personalized

    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">Question Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">Generate interview questions based on your resume</p>', unsafe_allow_html=True)

    resume = st.session_state.resume_data

    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        role = st.selectbox("Select Role", ROLES, key="q_role",
                            index=ROLES.index(st.session_state.role) if st.session_state.role in ROLES else 0)
    with c2:
        diff  = st.selectbox("Difficulty Level", DIFFICULTY_LEVELS, key="q_diff")
    with c3:
        count = st.selectbox("No. of Questions", [5, 10, 15, 20], index=1, key="q_count")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Generate Questions", type="primary", use_container_width=True):
            with st.spinner("Generating..."):
                qs = generate_generic(role, diff, count)
                st.session_state.questions    = qs
                st.session_state.role         = role
                st.session_state.personalized = False
            st.rerun()
    with c2:
        if resume:
            if st.button("✨ Personalized from My Resume", use_container_width=True):
                with st.spinner("Generating personalized questions..."):
                    qs = generate_personalized(
                        role, resume.get("found_skills",[]),
                        resume.get("top_skills",[])[:5], count)
                    st.session_state.questions    = qs
                    st.session_state.role         = role
                    st.session_state.personalized = True
                st.rerun()
        else:
            st.button("✨ Personalized (upload resume first)", disabled=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    questions = st.session_state.questions
    if not questions:
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:36px">💬</div><div style="color:#9C7A6B;margin-top:12px">Choose a role and click Generate Questions above.</div></div>', unsafe_allow_html=True)
        return

    if st.session_state.personalized:
        st.markdown('<div style="background:rgba(232,137,106,.12);border:1px solid #E8896A;color:#E8896A;border-radius:8px;padding:10px 16px;margin-bottom:12px;font-size:13px">✨ Questions <strong>personalized from your resume</strong> — tailored to your exact skills and projects.</div>', unsafe_allow_html=True)

    tech = [q for q in questions if q.get("category")=="Technical"]
    hr   = [q for q in questions if q.get("category")=="HR"]
    proj = [q for q in questions if q.get("category")=="Project Based"]
    cats = f'<span class="b-accent">All ({len(questions)})</span>'
    if tech: cats += f' <span class="b-cyan">Technical ({len(tech)})</span>'
    if hr:   cats += f' <span class="b-yellow">HR ({len(hr)})</span>'
    if proj: cats += f' <span class="b-accent">Project Based ({len(proj)})</span>'
    st.markdown(f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px">{cats}</div>', unsafe_allow_html=True)

    st.markdown('<div class="ai-card">', unsafe_allow_html=True)
    for i, q in enumerate(questions, 1):
        db = diff_badge(q.get("difficulty","Medium"))
        cb = f'<span class="b-accent">{q.get("category","")}</span>'
        pb = '<span class="b-cyan">✨</span>' if q.get("personalized") else ""
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid #F0DDD0">
          <span style="width:26px;height:26px;border-radius:50%;background:rgba(232,137,106,.2);
                       color:#E8896A;font-size:11px;font-weight:700;display:flex;align-items:center;
                       justify-content:center;flex-shrink:0;margin-top:2px">{i}</span>
          <span>
            <span style="display:block;font-size:13.5px;color:#3A2E2A;margin-bottom:6px">{q['question']}</span>
            {cb} {db} {pb}
          </span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    txt = "\n".join(
        [f"Interview Questions — {st.session_state.role}", "="*44, ""] +
        [f"{i}. [{q.get('category')}] [{q.get('difficulty')}] {q['question']}"
         for i, q in enumerate(questions, 1)]
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶️ Start Mock Interview", type="primary", use_container_width=True):
            st.session_state.current_q_index    = 0
            st.session_state.answers            = {}
            st.session_state.evaluations        = {}
            st.session_state.interview_started  = True
            st.session_state.interview_complete = False
            st.session_state.q_start_time       = time.time()
            try:
                from services.mock_interview import start_session
                start_session(st.session_state.session_id,
                              st.session_state.role,
                              questions,
                              st.session_state.personalized)
            except Exception:
                pass
            st.session_state.page = "mock"
            st.rerun()
    with c2:
        st.download_button("⬇️ Download Questions", data=txt,
                           file_name="interview_questions.txt",
                           mime="text/plain", use_container_width=True)


def page_mock_interview():
    questions = st.session_state.get("questions", [])
    if not questions:
        st.warning("No questions loaded. Please generate questions first.")
        if st.button("← Go to Question Generator"):
            st.session_state.page = "questions"; st.rerun()
        return

    idx   = st.session_state.get("current_q_index", 0)
    total = len(questions)

    if idx >= total:
        st.session_state.interview_complete = True
        st.session_state.page = "report"
        st.rerun()
        return

    question     = questions[idx]
    role         = st.session_state.get("role","Software Engineer")
    personalized = st.session_state.get("personalized", False)

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f'<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">Mock Interview</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#9C7A6B;font-size:13px">{role}{"  ✨ Personalized" if personalized else ""}</p>', unsafe_allow_html=True)
    with c2:
        if st.button("⏹ End Interview"):
            st.session_state.interview_complete = True
            try:
                from services.mock_interview import end_session
                end_session(st.session_state.session_id)
            except Exception:
                pass
            st.session_state.page = "report"; st.rerun()

    prog = round((idx / total) * 100)
    st.markdown(f"""
    <div style="margin-bottom:16px">
      <div style="display:flex;justify-content:space-between;font-size:12px;
                  color:#9C7A6B;margin-bottom:6px">
        <span>Question {idx+1} of {total}</span><span>{prog}% complete</span>
      </div>
      <div class="prog-bar"><div class="prog-fill" style="width:{prog}%"></div></div>
    </div>""", unsafe_allow_html=True)
    
    elapsed = int(time.time() - (st.session_state.get("q_start_time") or time.time()))
    remaining = max(0, 120 - elapsed)
    mins, secs = remaining // 60, remaining % 60
    tc = "#E8896A" if remaining > 30 else "#F59E0B" if remaining > 10 else "#EF4444"
    db = diff_badge(question.get("difficulty","Medium"))

    st.markdown(f"""
    <div class="ai-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <div style="display:flex;gap:8px">
          <span class="b-accent">{question.get('category','Technical')}</span>{db}
        </div>
        <div style="background:#FDEAE0;border:1px solid #E8C7AE;border-radius:12px;
                    padding:8px 18px;text-align:center">
          <div style="font-size:10px;color:#9C7A6B;text-transform:uppercase;letter-spacing:.5px">Time Left</div>
          <div style="font-size:24px;font-weight:700;color:{tc}">{mins:02d}:{secs:02d}</div>
        </div>
      </div>
      <p style="font-size:17px;font-weight:600;color:#3A2E2A;line-height:1.5;margin-bottom:12px">
        {question['question']}</p>
      <div class="waveform">
        {''.join(f'<span style="height:{h}%"></span>' for h in [20,55,85,40,70,30,90,55,35,75,45,80])}
      </div>
    </div>""", unsafe_allow_html=True)

    answer = st.text_area("Your Answer",
                          placeholder="Type your answer here. Be clear, concise and specific...",
                          height=130, key=f"ans_{idx}")
    st.caption("💡 Tip: Structure your answer as — explanation → example → takeaway.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📤 Submit Answer", type="primary", use_container_width=True):
            if answer.strip():
                _submit_answer(question, answer, idx, total)
            else:
                st.warning("Please write an answer before submitting.")
    with c2:
        if st.button("⏭ Skip to Report", use_container_width=True):
            st.session_state.interview_complete = True
            st.session_state.page = "report"; st.rerun()


def _submit_answer(question, answer, idx, total):
    from services.answer_evaluator import evaluate
    with st.spinner("Evaluating your answer..."):
        evaluation = evaluate(
            question["question"], answer,
            st.session_state.get("role","Software Engineer"),
            question.get("keywords"),
        )
    st.session_state.answers[idx]     = answer
    st.session_state.evaluations[idx] = evaluation
    try:
        from services.mock_interview import record_answer, advance
        record_answer(st.session_state.session_id, idx, answer, evaluation)
        advance(st.session_state.session_id, idx + 1)
    except Exception:
        pass
    st.session_state.current_eval    = {
        "question": question, "answer": answer,
        "evaluation": evaluation, "idx": idx, "total": total,
    }
    st.session_state.current_q_index = idx + 1
    st.session_state.q_start_time    = time.time()
    st.session_state.page            = "evaluation"
    st.rerun()


def page_evaluation():
    cur = st.session_state.get("current_eval")
    if not cur:
        st.session_state.page = "mock"; st.rerun(); return

    question   = cur["question"]
    answer     = cur["answer"]
    evaluation = cur["evaluation"]
    idx        = cur["idx"]
    total      = cur["total"]
    score      = evaluation.get("score", 0)

    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">AI Evaluation</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">Question {idx+1} of {total} · Your answer evaluation and feedback</p>', unsafe_allow_html=True)

    color = "#10B981" if score >= 7 else "#F59E0B" if score >= 5 else "#EF4444"
    badge = "b-green"  if score >= 7 else "b-yellow" if score >= 5 else "b-red"
    lbl   = "Good Answer" if score >= 7 else "Average" if score >= 5 else "Needs Work"
    stars = "★" * round(score/2) + "☆" * (5 - round(score/2))

    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
          {svg_ring(score, 10, size=100, color=color, sub="/10")}
          <div style="color:#F59E0B;font-size:16px;letter-spacing:2px">{stars}</div>
          <span class="{badge}">{lbl}</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-weight:600;color:#3A2E2A;margin-bottom:8px">Detailed Feedback</div>
          <p style="font-size:13px;color:#3A2E2A;line-height:1.9">{evaluation.get('feedback','')}</p>
        </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#10B981;font-weight:600;text-transform:uppercase;margin-bottom:12px">💪 Strengths</div>', unsafe_allow_html=True)
        for s in evaluation.get("strengths",[]):
            st.markdown(f'<div style="display:flex;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:13px;color:#3A2E2A"><span style="color:#10B981">✓</span>{s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#F59E0B;font-weight:600;text-transform:uppercase;margin-bottom:12px">📈 Areas to Improve</div>', unsafe_allow_html=True)
        for im in evaluation.get("improvements",[]):
            st.markdown(f'<div style="display:flex;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:13px;color:#3A2E2A"><span style="color:#F59E0B">↑</span>{im}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ai-card">
      <div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:8px">Question</div>
      <p style="font-weight:600;color:#3A2E2A;margin-bottom:14px">{question['question']}</p>
      <div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:8px">Your Answer</div>
      <p style="font-size:13px;color:#9C7A6B;line-height:1.9">{answer}</p>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        next_lbl = "Next Question →" if idx + 1 < total else "📋 View Final Report"
        if st.button(next_lbl, type="primary", use_container_width=True):
            if idx + 1 < total:
                st.session_state.page = "mock"
            else:
                st.session_state.interview_complete = True
                try:
                    from services.mock_interview import end_session
                    end_session(st.session_state.session_id)
                except Exception:
                    pass
                st.session_state.page = "report"
            st.rerun()
    with c2:
        if st.button("End & See Report", use_container_width=True):
            st.session_state.interview_complete = True
            st.session_state.page = "report"; st.rerun()


def page_final_report():
    from services.report_generator import build

    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">Final Interview Report</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">Overall performance in the interview</p>', unsafe_allow_html=True)

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
        st.markdown('<div class="ai-card" style="text-align:center;padding:48px"><div style="font-size:44px">📋</div><div style="color:#3A2E2A;font-size:15px;font-weight:500;margin-top:12px">No interview data yet</div><div style="color:#9C7A6B;margin-top:6px">Complete a mock interview first to generate your report.</div></div>', unsafe_allow_html=True)
        if st.button("Start Mock Interview →", type="primary"):
            st.session_state.page = "questions"; st.rerun()
        return

    os_val = report.get("overall_score", 0)
    lc     = "#10B981" if os_val >= 8 else "#E8896A" if os_val >= 6 else "#F59E0B"
    stars  = report.get("stars","")

    pers_badge  = '<span class="b-cyan" style="font-size:13px">✨ Personalized</span>' if report.get("personalized") else ""
    role_badge  = f'<span class="b-green" style="font-size:13px">{report.get("role","")}</span>' if report.get("role") else ""
    st.markdown(f"""
    <div class="ai-card" style="text-align:center;padding:36px">
      <div style="font-size:56px;font-weight:800;color:{lc};line-height:1">
        {os_val}<span style="font-size:22px;color:#9C7A6B">/10</span></div>
      <div style="color:#F59E0B;font-size:20px;letter-spacing:2px;margin:8px 0">{stars}</div>
      <div style="display:flex;gap:8px;justify-content:center;margin:10px 0">
        <span class="b-accent" style="font-size:13px">{report.get('performance_label','')}</span>
        {pers_badge} {role_badge}
      </div>
      <p style="color:#9C7A6B;font-size:13px;max-width:520px;margin:16px auto 0;line-height:1.9">
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
              <div style="font-size:22px;margin-bottom:6px">{icon}</div>
              <div style="font-size:28px;font-weight:700;color:#3A2E2A">{val}</div>
              <div style="font-size:12px;color:#9C7A6B">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:16px">Score Breakdown</div>', unsafe_allow_html=True)
        for lbl, sc in report.get("breakdown",{}).items():
            pc = int(sc/10*100)
            fc = "p-green" if sc >= 7 else "p-yellow" if sc < 5 else ""
            st.markdown(f"""
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:13px;color:#9C7A6B">{lbl}</span>
                <span style="font-size:13px;color:#3A2E2A;font-weight:600">{sc}/10</span>
              </div>
              <div class="prog-bar"><div class="prog-fill {fc}" style="width:{pc}%"></div></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        ats = report.get("ats_score", 0)
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:16px">Resume Performance</div>', unsafe_allow_html=True)
        if ats:
            combined = int(os_val/10*0.6*100 + ats/100*0.4*100)
            ag = "p-green" if ats >= 70 else ""
            ig = int(os_val/10*100)
            st.markdown(f"""
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:13px;color:#9C7A6B">ATS Resume Score</span>
                <span style="font-size:13px;color:#3A2E2A;font-weight:600">{ats}/100</span>
              </div>
              <div class="prog-bar"><div class="prog-fill {ag}" style="width:{ats}%"></div></div>
            </div>
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:13px;color:#9C7A6B">Interview Score</span>
                <span style="font-size:13px;color:#3A2E2A;font-weight:600">{os_val}/10</span>
              </div>
              <div class="prog-bar"><div class="prog-fill" style="width:{ig}%"></div></div>
            </div>
            <div class="ai-card-flat" style="text-align:center">
              <div style="font-size:12px;color:#9C7A6B;margin-bottom:4px">Combined Readiness</div>
              <div style="font-size:32px;font-weight:700;color:#E8896A">{combined}%</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:13px">Upload a resume to see combined score.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    qs    = st.session_state.get("questions",[])
    evals = st.session_state.get("evaluations",{})
    if qs:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">Q&A Review</div>', unsafe_allow_html=True)
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
                                 color:#E8896A;font-size:11px;font-weight:700;display:flex;align-items:center;
                                 justify-content:center;flex-shrink:0">{i+1}</span>
                    <span style="font-weight:600;font-size:13px;color:#3A2E2A">{q['question']}</span>
                  </div>
                  <div style="display:flex;gap:8px;align-items:center;padding-left:36px">
                    <span class="{eb}">{es}/10</span>
                    <span style="font-size:12px;color:#9C7A6B">{fb}…</span>
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid #F0DDD0"><span style="font-size:13px;color:#9C7A6B">{i+1}. {q["question"]}</span> <span class="b-yellow">Not answered</span></div>', unsafe_allow_html=True)
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


def page_career_dashboard():
    st.markdown('<h1 style="color:#3A2E2A;font-size:22px;margin-bottom:2px">Career Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:13px;margin-bottom:20px">Your career-readiness snapshot, all in one place</p>', unsafe_allow_html=True)

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
      <div style="font-size:12px;color:#9C7A6B;font-weight:600;text-transform:uppercase;letter-spacing:.5px">Overall Career Readiness</div>
      <div style="font-size:52px;font-weight:800;color:#E8896A;line-height:1;margin-top:8px">{readiness}%</div>
      <p style="color:#9C7A6B;font-size:13px;max-width:520px;margin:12px auto 0;line-height:1.8">
        Combines your ATS resume score, mock interview performance, best career-path match, and latest job-description match.</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        color = "#10B981" if ats >= 70 else "#F59E0B" if ats >= 50 else "#EF4444"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:11px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">📄 ATS Score</div>
          <div style="font-size:26px;font-weight:700;color:{color}">{ats}<span style="font-size:12px;color:#9C7A6B">/100</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_ats", use_container_width=True): st.session_state.page="ats"; st.rerun()

    with c2:
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:11px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">🎤 Mock Interview</div>
          <div style="font-size:26px;font-weight:700;color:#E8896A">{mock_avg}<span style="font-size:12px;color:#9C7A6B">/10</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_mock", use_container_width=True): st.session_state.page="report"; st.rerun()

    with c3:
        label = top_path["title"] if top_path else "Not analysed"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:11px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">🧭 Best Career Fit</div>
          <div style="font-size:16px;font-weight:700;color:#3A2E2A;margin-bottom:4px">{label}</div>
          <div style="font-size:13px;color:#10B981;font-weight:600">{top_pct}% match</div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_career", use_container_width=True): st.session_state.page="career"; st.rerun()

    with c4:
        label = f"{jm_pct}% match" if jobmatch else "Not analysed"
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-size:11px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:6px">🎯 Latest Job Match</div>
          <div style="font-size:26px;font-weight:700;color:#E8896A">{label}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("View →", key="d_jm", use_container_width=True): st.session_state.page="jobmatch"; st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">🗺️ Learning Roadmap Progress</div>', unsafe_allow_html=True)
        if roadmap:
            st.markdown(f"""
            <p style="font-size:13px;color:#3A2E2A;line-height:1.8">
              Your <strong>{weeks_left}-week</strong> roadmap for <strong>{roadmap['role']}</strong> covers
              <strong style="color:#E8896A">{roadmap['total_skills']}</strong> skills across
              {len(roadmap.get('milestones', []))} milestones.</p>""", unsafe_allow_html=True)
            if st.button("Open Roadmap →", key="d_roadmap_open"):
                st.session_state.page = "roadmap"; st.rerun()
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:13px">No roadmap generated yet.</p>', unsafe_allow_html=True)
            if st.button("Generate Roadmap →", key="d_roadmap_gen"):
                st.session_state.page = "roadmap"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ai-card"><div style="font-size:12px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:12px">🧭 Top 3 Career Matches</div>', unsafe_allow_html=True)
        if career and career.get("top_matches"):
            for p in career["top_matches"][:3]:
                pc = p["match_percent"]
                fc = "p-green" if pc >= 70 else "p-yellow" if pc >= 40 else ""
                st.markdown(f"""
                <div style="margin-bottom:12px">
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="font-size:13px;color:#3A2E2A">{p['title']}</span>
                    <span style="font-size:13px;color:#9C7A6B;font-weight:600">{pc}%</span>
                  </div>
                  <div class="prog-bar"><div class="prog-fill {fc}" style="width:{pc}%"></div></div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#9C7A6B;font-size:13px">No career recommendations yet.</p>', unsafe_allow_html=True)
            if st.button("Get Recommendations →", key="d_career_gen"):
                st.session_state.page = "career"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    load_css()
    init_session()

    with st.sidebar:
        render_sidebar()

    pages = {
        "home":       page_home,
        "ats":        page_ats_checker,
        "analysis":   page_resume_analysis,
        "career":     page_career_recommendation,
        "roadmap":    page_learning_roadmap,
        "jobmatch":   page_job_match_analyzer,
        "questions":  page_question_generator,
        "mock":       page_mock_interview,
        "evaluation": page_evaluation,
        "report":     page_final_report,
        "dashboard":  page_career_dashboard,
    }
    pages.get(st.session_state.page, page_home)()


if __name__ == "__main__":
    main()
