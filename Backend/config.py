import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GOOGLE_CLIENT_KEY = os.getenv("GOOGLE_CLIENT_KEY")
    BACKEND_KEY = os.getenv("BACKEND_KEY")