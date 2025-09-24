from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Contract Analyzer API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"pdf"}
    UPLOAD_FOLDER: str = "uploads"
    
    # OpenAI settings
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()