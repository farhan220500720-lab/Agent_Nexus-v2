from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Core LLM
    GEMINI_API_KEY: str = Field(..., validation_alias="GEMINI_API_KEY")

    # Redis (Dramatiq)
    REDIS_DSN: str = Field("redis://redis:6379/0", validation_alias="REDIS_DSN")

    # PostgreSQL Database Components
    POSTGRES_USER: str = Field(..., validation_alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., validation_alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., validation_alias="POSTGRES_DB")
    POSTGRES_HOST: str = Field("db", validation_alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, validation_alias="POSTGRES_PORT")

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """
        Constructs the full SQLAlchemy connection string from component parts.
        This is what Alembic and the SQLAlchemy engine need.
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
