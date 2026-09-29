from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-this-secret-key"
    database_url: str = f"sqlite:///{BASE_DIR / 'pocketsmart.db'}"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    access_token_expire_minutes: int = 120
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
