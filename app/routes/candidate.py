from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database import models
from app.agents import question_agent, scoring_agent
from app.schemas.candidate import CandidateCreate, AnswerCreate, InterviewResult
from app.core.config import FINAL_THRESHOLD

router = APIRouter()

@router.post("/register")
def register_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter_by(email=payload.email, role=payload.role).first()
    if candidate:
        return {"candidate_id": candidate.id, "message": "Candidate already registered."}
    candidate = models.Candidate(
        name=payload.name,
        email=payload.email,
        role=payload.role,
        cv_text=payload.cv_text
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return {"candidate_id": candidate.id, "message": "Registered successfully."}

@router.post("/generate_question/{candidate_id}")
def generate_question_endpoint(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter_by(id=candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    question = question_agent.generate_question(candidate.role, candidate.cv_text)
    return {"question": question}

@router.post("/submit_answer/{candidate_id}")
def submit_answer(candidate_id: int, payload: AnswerCreate, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter_by(id=candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    score = scoring_agent.evaluate_answer(candidate.role, payload.question, payload.answer)
    interview = models.Interview(candidate_id=candidate_id, question=payload.question, answer=payload.answer, score=score)
    db.add(interview)
    db.commit()
    db.refresh(interview)

    # Calculate total score
    interviews = db.query(models.Interview).filter_by(candidate_id=candidate_id).all()
    total_score = sum(i.score for i in interviews)
    max_score = sum(i.max_score for i in interviews)
    percentage = (total_score / max_score) * 100 if max_score else 0
    final_status = "Selected for final viva" if percentage >= FINAL_THRESHOLD else "Review Needed"

    return {"score": score, "percentage": percentage, "final_status": final_status}