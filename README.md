# CareerPilot AI

An AI-powered career readiness platform — not just an interview prep tool.
It scores your resume against ATS systems, recommends career paths, builds
a personalized learning roadmap, matches you against real job descriptions,
runs mock interviews with AI-evaluated answers, and rolls everything up into
a single career-readiness dashboard. Built with Streamlit, MongoDB, and the
OpenAI API (GPT-4o-mini), with rule-based fallbacks so it works fully offline.

🔗 **Live Demo:** https://careerpilot-ai-n2cudmco5jdcge7dmy5459.streamlit.app/
🔗 **Repo:** https://github.com/kushant451/CareerPilot-AI

## Features

**Resume Intelligence**
- ATS resume scoring (0–100) — checks section structure and keyword density against role-specific skill banks
- Resume analysis — strengths, weaknesses, top skills, and detected project names extracted from resume text
- Resume validation — rejects non-resume documents (invoices, certificates, tickets, etc.) before analysis

**Career Guidance**
- Career path recommendation — ranks career paths by skill match percentage, with matched/missing skills per path
- Skill gap analysis — flags missing skills by priority and links each to a learning resource
- Personalized learning roadmap — generates a week-by-week study plan targeting your skill gaps
- Job description match analyzer — compares your resume against a pasted job description and scores the match

**Interview Practice**
- Personalized interview questions generated from your actual resume content and detected skills
- Generic question bank by role and difficulty (Easy / Medium / Hard)
- Mock interview flow with live timer and AI-evaluated answers
- Per-answer feedback with strengths, improvements, and a numeric score
- Final interview report with score breakdown, accuracy, and a downloadable summary

**Dashboard**
- Career Dashboard — combines ATS score, mock interview average, best career-path match, and job-match score into one overall readiness percentage

**Persistence**
- MongoDB Atlas-backed session and history persistence across resumes, interviews, career recommendations, roadmaps, and job matches

## Tech Stack

Python · Streamlit · MongoDB Atlas (pymongo) · OpenAI API (GPT-4o-mini) · pdfplumber · python-docx · Pytest

## Run Locally

```bash
git clone https://github.com/kushant451/CareerPilot-AI.git
cd CareerPilot-AI
pip install -r requirements.txt
streamlit run app.py
```

Create a `.env` file (get `MONGO_URI` from your MongoDB Atlas cluster's "Connect" → "Drivers" screen):

```
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=careerpilot_ai
OPENAI_API_KEY=
SECRET_KEY=your-random-secret-key
```

The app runs fully offline without an OpenAI key — questions, evaluations,
career recommendations, and roadmaps all fall back to rule-based /
data-driven engines, so `OPENAI_API_KEY` is optional.

## Project Structure

```
app.py            → Streamlit entry point, page router
ui/               → Pages, sidebar, session state, shared widgets and styles
  pages/          → home, ats, analysis, career, roadmap, jobmatch,
                     questions, mock, evaluation, report, dashboard
config/           → settings, MongoDB collection names, LLM config
database/         → MongoDB connection and collection accessors
services/         → ATS scoring, resume parsing/validation/analysis,
                     career recommendation, skill gap analysis, roadmap
                     generation, job match analysis, question generation,
                     answer evaluation, report generation
ai_engine/        → LLM client and prompt templates (with fallback logic)
utils/            → logging, file handling, text cleaning, helpers
data/             → skill keyword bank, career paths, question bank
tests/            → unit tests
```

## Pages / Navigation

| Page | Description |
|---|---|
| Home | Upload a resume and select a target role to kick off analysis |
| ATS Checker | Resume score against role-specific keyword and section checks |
| Resume Analysis | Strengths, weaknesses, top skills, detected projects |
| Career Recommendation | Best-matching career paths ranked by skill overlap |
| Learning Roadmap | Week-by-week plan to close skill gaps for a target role |
| Job Match Analyzer | Match your resume against a pasted job description |
| Question Generator | Generic or resume-personalized interview questions |
| Mock Interview | Timed Q&A session with AI-evaluated answers |
| Final Report | Score breakdown, accuracy, and downloadable summary |
| Career Dashboard | Aggregated career-readiness score across all modules |

## Testing

```bash
python -m pytest tests/ -v
```

## What I Learned

Building the ATS scoring engine taught me how applicant tracking systems
actually evaluate resumes — matching section structure and keyword density
rather than just "reading" content. I also designed the MongoDB schema to
track resumes, interviews, career recommendations, roadmaps, job matches,
and history as separate collections linked by a session ID, so a user's
data persists across every page without needing full authentication.
Adding rule-based fallbacks for every AI-powered feature (questions,
evaluation, career matching, roadmaps) made the app fully usable without
an API key, which shaped how I separated "AI enhancement" from "core logic"
throughout the codebase.

## License

MIT