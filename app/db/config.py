from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Настройки для БД PostgreSQL
    """

    POSTGRES_URL: str = "postgresql+asyncpg://test_1:test@localhost:5433/ria_energo_test"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
