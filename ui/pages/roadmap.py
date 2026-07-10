"""Learning roadmap generator page."""
import streamlit as st

from ui.db_helpers import save_roadmap_to_db

def page_learning_roadmap():
    from config.settings import ROLES
    from services.roadmap_generator import generate

    st.markdown('<h1 style="color:#3A2E2A;font-size:25px;margin-bottom:2px">Learning Roadmap</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9C7A6B;font-size:15px;margin-bottom:20px">A week-by-week plan to close your skill gaps</p>', unsafe_allow_html=True)

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
        st.markdown('<div class="ai-card" style="text-align:center;padding:40px"><div style="font-size:39px">🗺️</div><div style="color:#9C7A6B;margin-top:12px">Click "Generate Roadmap" to build your learning plan.</div></div>', unsafe_allow_html=True)
        return

    ai_tag = '<span class="b-cyan">✨ AI Generated</span>' if result.get("generated_by_ai") else '<span class="b-accent">Curated Plan</span>'
    st.markdown(f"""
    <div style="display:flex;gap:10px;align-items:center;margin:14px 0">
      <span class="b-green">{result['weeks']} Weeks</span>
      <span class="b-accent">{result['total_skills']} Skills</span>
      {ai_tag}
    </div>""", unsafe_allow_html=True)

    for m in result.get("milestones", []):
        skills_tags = "".join(f'<span class="tag">{s}</span>' for s in m.get("skills", [])) or '<span style="color:#9C7A6B;font-size:13.5px">Review & practice</span>'
        tasks_html = "".join(f'<div style="padding:4px 0;font-size:14px;color:#3A2E2A">☐ {t}</div>' for t in m.get("tasks", []))
        res_html = "".join(f'<a href="{r["url"]}" target="_blank" style="color:#E8896A;font-size:13px;margin-right:10px">🔗 {r["skill"]}</a>' for r in m.get("resources", []))
        st.markdown(f"""
        <div class="ai-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <span style="width:30px;height:30px;border-radius:50%;background:rgba(232,137,106,.2);
                         color:#E8896A;font-size:13.5px;font-weight:700;display:flex;align-items:center;
                         justify-content:center;flex-shrink:0">{m.get('week','?')}</span>
            <span style="font-weight:700;font-size:16.5px;color:#3A2E2A">{m.get('title','')}</span>
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
