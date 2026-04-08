from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Настройки приложения"""
    model_config = SettingsConfigDict(
        env_file=".env", #BASE_DIR / ".env"
        env_prefix="",
        case_sensitive=False,
    )

    APP_NAME: str = 'Project'
    APP_DEBUG: bool = False
    ENV: str 

    SQLITE_PATH: str 

    JWT_SECRET: str 
    JWT_ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str 
    OPENROUTER_MODEL: str 
    OPENROUTER_SITE_URL: Optional[str] = None
    OPENROUTER_APP_NAME: Optional[str] = None

settings = Settings()

def get_database_url() -> str:
    """Формирует URL для подключения к БД"""
    return f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"
