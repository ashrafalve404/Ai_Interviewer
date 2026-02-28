from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)
    cv_text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    interviews = relationship("Interview", back_populates="candidate")

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    question = Column(String)
    answer = Column(String)
    score = Column(Float)
    max_score = Column(Float, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    candidate = relationship("Candidate", back_populates="interviews")