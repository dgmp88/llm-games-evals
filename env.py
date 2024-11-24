from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    STOCKFISH_PATH: str = Field(description="Path to the Stockfish binary")
    # Check it exists

    @field_validator("STOCKFISH_PATH")
    @classmethod
    def check_stockfish_path(cls, v: str) -> str:
        if not Path(v).exists():
            raise ValueError(f"Stockfish path {v} does not exist")
        return v

    OPENAI_API_KEY: str = Field(description="OpenAI API key")


env = Env()
