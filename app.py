import streamlit as st

from ui.styles import load_css
from ui.session import init_session
from ui.sidebar import render_sidebar

from ui.pages.home import page_home
from ui.pages.ats import page_ats_checker
from ui.pages.analysis import page_resume_analysis
from ui.pages.career import page_career_recommendation
from ui.pages.roadmap import page_learning_roadmap
from ui.pages.jobmatch import page_job_match_analyzer
from ui.pages.questions import page_question_generator
from ui.pages.mock import page_mock_interview
from ui.pages.evaluation import page_evaluation
from ui.pages.report import page_final_report
from ui.pages.dashboard import page_career_dashboard

st.set_page_config(
    page_title="AI Interview Prep",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
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


def main():
    load_css()
    init_session()

    with st.sidebar:
        render_sidebar()

    PAGES.get(st.session_state.page, page_home)()


if __name__ == "__main__":
    main()
