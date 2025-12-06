from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(base_dir, '..', '..', '.env'),
        env_file_encoding='utf-8'
    )

    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="agent_nexus_db")
    POSTGRES_HOST: str = Field(default="db")
    POSTGRES_PORT: int = Field(default=5432)
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    REDIS_DSN: str = Field(default="redis://redis:6379/0")

    GEMINI_API_KEY: str = Field(default="YOUR_GEMINI_API_KEY") 

    QDRANT_HOST: str = Field(default="qdrant")
    QDRANT_PORT: int = Field(default=6333)

settings = Settings()