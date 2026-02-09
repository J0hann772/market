from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):

    DEBUG: bool = False
    URL_DATABASE: str

    SECRET_KEY: str = "placeholder_key"
    ALGO: str = "HS256"
    EXPIRE_MIN: int = 30


    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        extra="ignore"
    )


settings = Settings()

