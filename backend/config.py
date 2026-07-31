import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FOLDER = BASE_DIR / "outputs"

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Dataset Intelligence Copilot"

    # ==========================================
    # Featherless AI Configuration
    # ==========================================
    FEATHERLESS_API_KEY: str = ""
    FEATHERLESS_BASE_URL: str = "https://api.featherless.ai/v1"

    # Recommended hackathon model
    FEATHERLESS_MODEL: str = "deepseek-ai/DeepSeek-V3.2"

    # ==========================================
    # Upload Settings
    # ==========================================
    UPLOAD_FOLDER: Path = BASE_DIR / "uploads"
    OUTPUT_FOLDER: Path = BASE_DIR / "outputs"
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: set = {".csv"}

    # ==========================================
    # Database
    # ==========================================
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/history.db"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

# Ensure upload directory exists
settings.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)