from fastapi import FastAPI
from app.routes import candidate

app = FastAPI(title="AI Interviewer MVP")

app.include_router(candidate.router, prefix="/api/candidate", tags=["Candidate"])