from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    redis_hostname: str
    redis_port: str
    redis_password: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"

settings = Settings()