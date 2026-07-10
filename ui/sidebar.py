"""Left navigation sidebar."""
import streamlit as st

def render_sidebar():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;padding:8px 0 20px;
                border-bottom:1px solid #F0DDD0;margin-bottom:12px'>
      <div style='width:60px;height:60px;border-radius:15px;background:#E8896A;
                  display:flex;align-items:center;justify-content:center;font-size:31px'>🤖</div>
      <div>
        <div style='font-size:27px;font-weight:900;color:#3A2E2A'>AI Interview</div>
        <div style='font-size:18px;color:#9C7A6B'>Preparation Assistant</div>
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
      <div style='font-size:12.5px;color:#F59E0B;font-weight:600;margin-bottom:4px'>⭐ Pro Features</div>
      <div style='font-size:13px;color:#9C7A6B;margin-bottom:10px'>
        Unlimited mock interviews, AI feedback & analytics.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  New Session", use_container_width=True, key="nav_reset"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
