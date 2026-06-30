# AI Interview Preparation Assistant

AI-powered tool that analyzes resumes, generates personalized interview 
questions, and evaluates mock interview answers using GPT-4o-mini.

🔗 **Live Demo:** https://your-app.streamlit.app

## Features

- ATS resume scoring (0-100) against role-specific keyword banks
- Resume analysis — strengths, weaknesses, and skill gap detection
- Personalized interview questions generated from your actual resume content
- Generic question bank by role and difficulty (Easy/Medium/Hard)
- Mock interview with live timer and AI-evaluated answers
- Detailed feedback with strengths and areas to improve per answer
- Final interview report with score breakdown and downloadable summary
- MongoDB-backed session and history persistence

## Tech Stack

Python · Streamlit · MongoDB · OpenAI API (GPT-4o-mini) · pdfplumber · python-docx · Pytest

## Run Locally

```bash
git clone https://github.com/kushant451/CareerPilot-AI.git
cd CareerPilot-AI
pip install -r requirements.txt
streamlit run app.py
```

Create a `.env` file:

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=careerpilot_ai
OPENAI_API_KEY=
SECRET_KEY=your-random-secret-key
```

The app runs fully offline without an OpenAI key — questions and 
evaluation fall back to a rule-based engine, so OpenAI is optional.

## Project Structure

```
app.py            → Streamlit entry point
config/           → settings, MongoDB and LLM config
database/         → MongoDB connection and collections
services/         → ATS scoring, resume parsing, question generation,
                     answer evaluation, report generation
ai_engine/        → LLM client and prompt templates
utils/            → logging, file handling, text cleaning
data/             → skill keyword bank and question bank
tests/            → unit tests
```

## Testing

```bash
python -m pytest tests/ -v
```

## What I Learned

Building the ATS scoring engine taught me how applicant tracking systems
actually evaluate resumes — matching section structure and keyword 
density rather than just "reading" content. I also designed the MongoDB
schema to track resume, interview, and history as separate collections
linked by a session ID, so the same user's data persists across pages
without needing full authentication.

## License

MIT