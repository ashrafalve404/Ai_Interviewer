import openai
from app.core.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def evaluate_answer(role: str, question: str, candidate_answer: str):
    prompt = f"""
You are an AI interviewer.
Evaluate the candidate answer for the role {role}.
Question: {question}
Candidate Answer: {candidate_answer}
Return only a score from 0 to 10.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0,
        max_tokens=10
    )
    score_text = response['choices'][0]['message']['content'].strip()
    try:
        score = float(score_text)
    except:
        score = 0
    return score