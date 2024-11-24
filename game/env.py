from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PARENT_DIR = Path(__file__).parent.parent
RESULTS_DIR = PARENT_DIR / "results"

assert RESULTS_DIR.exists(), f"Results dir {RESULTS_DIR} does not exist"

ENV_FILE = PARENT_DIR / ".env"


class Env(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    STOCKFISH_PATH: str = Field(description="Path to the Stockfish binary")
    # Check it exists

    @field_validator("STOCKFISH_PATH")
    @classmethod
    def check_stockfish_path(cls, v: str) -> str:

        if not Path(v).exists():
            altpath = PARENT_DIR / v
            if not altpath.exists():
                raise ValueError(f"Stockfish path {v} does not exist")
        return v

    OPENAI_API_KEY: str = Field(description="OpenAI API key")
    ANTHROPIC_API_KEY: str = Field(description="Anthropic API key")
    GEMINI_API_KEY: str = Field(description="Gemini API key")
    TOGETHERAI_API_KEY: str = Field(description="TogetherAI API key")


env = Env()
