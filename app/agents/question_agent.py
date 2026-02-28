import openai
from app.core.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_question(role: str, cv_text: str):
    prompt = f"""
You are an AI interviewer.
Generate a relevant interview question for a candidate applying as {role}, considering their resume: {cv_text}.
Return ONLY the question as a string.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.5,
        max_tokens=100
    )
    question = response['choices'][0]['message']['content'].strip()
    return question