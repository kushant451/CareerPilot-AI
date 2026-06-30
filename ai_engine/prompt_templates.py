def question_generation_prompt(role, difficulty, count):
    level = ("mixing Easy, Medium and Hard" if difficulty == "All Levels"
             else f"at {difficulty} difficulty")
    return (
        f"Generate exactly {count} interview questions for a {role} role, {level}.\n"
        "Mix Technical, HR, and Project Based categories.\n"
        "Return ONLY a valid JSON array, no extra text, no markdown fences.\n"
        'Format: [{"question":"...","category":"Technical","difficulty":"Medium","keywords":["..."]}]'
    )

def personalized_question_prompt(role, skills, projects, count):
    skill_str   = ", ".join(skills[:20])  if skills   else "general programming"
    project_str = ", ".join(projects[:5]) if projects else "personal projects"
    return (
        f"You are an interviewer preparing personalized questions for a {role} candidate.\n"
        f"Their skills: {skill_str}.\nTheir projects: {project_str}.\n"
        f"Generate exactly {count} questions tailored to THEIR specific skills and projects.\n"
        "Return ONLY a valid JSON array, no extra text, no markdown fences.\n"
        'Format: [{"question":"...","category":"Technical","difficulty":"Medium","keywords":["..."]}]'
    )

def answer_evaluation_prompt(role, question, answer):
    return (
        f"You are an expert interviewer evaluating a {role} candidate.\n"
        f"Question: {question}\nCandidate's answer: {answer}\n\n"
        "Return ONLY a valid JSON object, no extra text.\n"
        '{"score":7,"strengths":["..."],"improvements":["..."],"feedback":"2-3 sentences"}'
    )

def resume_summary_prompt(resume_text, role):
    return (
        f"Analyse this resume for a {role} role in 2-3 sentences. "
        "Highlight the strongest asset and most important thing to fix.\n"
        f"Return ONLY plain text.\n\nResume:\n{resume_text[:3000]}"
    )