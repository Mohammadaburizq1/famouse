from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Service"
    API_V1_PREFIX: str = "/api/v1"

    # 🔐 JWT settings (with type hints!)
    SECRET_KEY: str = "c40cc1a7f1a8b6eb12c4a156c4416a27858878b08907d1dbe215c99209531d91"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Pydantic v2 style config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
