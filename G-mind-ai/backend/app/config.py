from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    google_api_key: str = ""
    llm_model: str = "gemini-3.7-flash"
    embedding_model: str = "gemini-embedding-2-preview"
    chroma_dir: str = "data/chroma"
    upload_dir: str = "data/uploads"
    chunk_size: int = 1000
    chunk_overlap: int = 150
    max_upload_mb: int = 25
    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
