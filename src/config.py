from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int  # ✅ Ensure it's an integer
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# ✅ Create a global settings instance
Config = Settings()
