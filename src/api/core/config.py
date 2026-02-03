from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENVIRONNEMENT: str = "development"
    DB_URL: str
    DB_PASSWORD: str
    APP_VERSION: str = "0.1.0"
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    POSTGRES_SCHEMA: str = "public"

    model_config = SettingsConfigDict(
        env_file=".env.load",
        extra="ignore" 
    )

settings = Settings()