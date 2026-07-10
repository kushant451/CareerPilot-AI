"""Interview question generator page."""
import time
import streamlit as st

from ui.widgets import diff_badge

def page_question_generator():
    from config.settings import ROLES, DIFFICULTY_LEVELS
    from services.question_generator import generate_generic, generate_personalized

    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">Question Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">Generate interview questions based on your resume</p>', unsafe_allow_html=True)

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
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:39px">💬</div><div style="color:#9C7A6B;margin-top:12px">Choose a role and click Generate Questions above.</div></div>', unsafe_allow_html=True)
        return

    if st.session_state.personalized:
        st.markdown('<div style="background:rgba(232,137,106,.12);border:1px solid #E8896A;color:#E8896A;border-radius:8px;padding:10px 16px;margin-bottom:12px;font-size:15px">✨ Questions <strong>personalized from your resume</strong> — tailored to your exact skills and projects.</div>', unsafe_allow_html=True)

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
                       color:#E8896A;font-size:12.5px;font-weight:700;display:flex;align-items:center;
                       justify-content:center;flex-shrink:0;margin-top:2px">{i}</span>
          <span>
            <span style="display:block;font-size:15.5px;color:#3A2E2A;margin-bottom:6px">{q['question']}</span>
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
