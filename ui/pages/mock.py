"""Live mock-interview page: timer, question, answer submission."""
import time
import streamlit as st

from ui.widgets import diff_badge

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
        st.markdown(f'<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">Mock Interview</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#9C7A6B;font-size:15px">{role}{"  ✨ Personalized" if personalized else ""}</p>', unsafe_allow_html=True)
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
      <div style="display:flex;justify-content:space-between;font-size:13.5px;
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
          <div style="font-size:11.5px;color:#9C7A6B;text-transform:uppercase;letter-spacing:.5px">Time Left</div>
          <div style="font-size:27px;font-weight:700;color:{tc}">{mins:02d}:{secs:02d}</div>
        </div>
      </div>
      <p style="font-size:19px;font-weight:600;color:#3A2E2A;line-height:1.5;margin-bottom:12px">
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
