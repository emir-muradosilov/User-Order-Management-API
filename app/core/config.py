
from pydantic_settings import BaseSettings
from fastapi.security import HTTPBearer
from typing import List


class Settings(BaseSettings):
    # JWT
    JWT_ALGORITHM: str = 'HS256'
    JWT_SECRET_KEY: str
    JWT_TOKEN_LOCATION: List[str] = ['headers']

    # Tokens
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = "ignore"  # 🔹 разрешаем лишние переменные


settings = Settings()

security = HTTPBearer()