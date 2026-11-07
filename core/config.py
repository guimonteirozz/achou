from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Achou! Marketplace"
    VERSION: str = "1.0.0"
    # Atualizado com a sua senha do PostgreSQL (12345)
    DATABASE_URL: str = "postgresql+psycopg://postgres:12345@localhost:5432/achou_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()