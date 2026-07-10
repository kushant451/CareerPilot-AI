"""Per-answer AI evaluation page shown right after each submission."""
import streamlit as st

from ui.widgets import svg_ring

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

    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">AI Evaluation</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">Question {idx+1} of {total} · Your answer evaluation and feedback</p>', unsafe_allow_html=True)

    color = "#10B981" if score >= 7 else "#F59E0B" if score >= 5 else "#EF4444"
    badge = "b-green"  if score >= 7 else "b-yellow" if score >= 5 else "b-red"
    lbl   = "Good Answer" if score >= 7 else "Average" if score >= 5 else "Needs Work"
    stars = "★" * round(score/2) + "☆" * (5 - round(score/2))

    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
          {svg_ring(score, 10, size=100, color=color, sub="/10")}
          <div style="color:#F59E0B;font-size:18px;letter-spacing:2px">{stars}</div>
          <span class="{badge}">{lbl}</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="ai-card">
          <div style="font-weight:600;color:#3A2E2A;margin-bottom:8px">Detailed Feedback</div>
          <p style="font-size:15px;color:#3A2E2A;line-height:1.9">{evaluation.get('feedback','')}</p>
        </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#10B981;font-weight:600;text-transform:uppercase;margin-bottom:12px">💪 Strengths</div>', unsafe_allow_html=True)
        for s in evaluation.get("strengths",[]):
            st.markdown(f'<div style="display:flex;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:15px;color:#3A2E2A"><span style="color:#10B981">✓</span>{s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ai-card"><div style="font-size:13.5px;color:#F59E0B;font-weight:600;text-transform:uppercase;margin-bottom:12px">📈 Areas to Improve</div>', unsafe_allow_html=True)
        for im in evaluation.get("improvements",[]):
            st.markdown(f'<div style="display:flex;gap:8px;padding:6px 0;border-bottom:1px solid #F0DDD0;font-size:15px;color:#3A2E2A"><span style="color:#F59E0B">↑</span>{im}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ai-card">
      <div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:8px">Question</div>
      <p style="font-weight:600;color:#3A2E2A;margin-bottom:14px">{question['question']}</p>
      <div style="font-size:13.5px;color:#9C7A6B;font-weight:500;text-transform:uppercase;margin-bottom:8px">Your Answer</div>
      <p style="font-size:15px;color:#9C7A6B;line-height:1.9">{answer}</p>
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
