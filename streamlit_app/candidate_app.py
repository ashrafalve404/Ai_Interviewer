import streamlit as st
import requests

st.title("AI Interviewer Portal")

name = st.text_input("Name")
email = st.text_input("Email")
role = st.text_input("Role Applied")
cv_text = st.text_area("Paste your CV / Resume text")

if st.button("Register"):
    res = requests.post("http://localhost:8000/api/candidate/register",
                        json={"name": name, "email": email, "role": role, "cv_text": cv_text})
    data = res.json()
    st.write(data)
    if "candidate_id" in data:
        st.session_state.candidate_id = data["candidate_id"]

if "candidate_id" in st.session_state:
    if st.button("Get Question"):
        res = requests.post(f"http://localhost:8000/api/candidate/generate_question/{st.session_state.candidate_id}")
        question = res.json()["question"]
        st.session_state.current_question = question
        st.write("Question:", question)

    answer = st.text_area("Your Answer")
    if st.button("Submit Answer") and st.session_state.current_question:
        payload = {"question": st.session_state.current_question, "answer": answer}
        res = requests.post(f"http://localhost:8000/api/candidate/submit_answer/{st.session_state.candidate_id}",
                            json=payload)
        st.write(res.json())