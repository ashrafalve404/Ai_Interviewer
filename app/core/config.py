import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_URL = os.getenv("DB_URL", "sqlite:///./sqlite.db")
QUESTION_TIME_LIMIT = 120  # seconds per question
FINAL_THRESHOLD = 70  # %