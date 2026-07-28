import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Dataset Intelligence Copilot"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Upload Settings
    UPLOAD_FOLDER: Path = BASE_DIR / "uploads"
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: set = {".csv"}
    
    # Database Settings
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/history.db"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Ensure upload directory exists
settings.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
