from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    APP_NAME: str = "CareerPilot AI"
    APP_VERSION: str = "1.0.0"
    # Production-safe default. Enable locally via DEBUG=True in .env to turn
    # on SQLAlchemy engine echo and verbose behaviour.
    DEBUG: bool = False

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-opus-4-8"

    # How often the daily discovery + tailoring pipeline runs, in hours.
    DAILY_PIPELINE_INTERVAL_HOURS: int = 24

    # Auto Apply drives a real headless browser to a live company application
    # page and fills it with the visitor's info. Defaults to on for local
    # dev; set to false for any deployment strangers can reach (e.g. a
    # public demo), since you don't want a random visitor's click launching
    # a browser against a real company's site. When false, matching jobs
    # are still tailored and saved, just never handed to the automation step.
    AUTO_APPLY_ENABLED: bool = True

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

    @property
    def DATABASE_URL(self) -> str:
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        ).render_as_string(hide_password=False)

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()