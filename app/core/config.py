from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Настройки приложения
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    POSTGRES_URL: str = "postgresql+asyncpg://test_1:test@localhost:5433/ria_energo_test"

    # Настройки Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"  # Пароль приложения, не аккаунта!
    SMTP_FROM_EMAIL: EmailStr = "noreply@example.com"

    class Config:
        env_file = ".env"  # Чтение переменных из файла .env

settings = Settings()