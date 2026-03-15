from enum import StrEnum

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings


class LLMProvider(StrEnum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GITHUB = "github"


class CampaignStatus(StrEnum):
    DRAFT = "draft"
    RUNNING = "running"
    RESEARCHED = "researched"
    STRATEGIZED = "strategized"
    PLANNED = "planned"
    COMPLETED = "completed"
    FAILED = "failed"


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    llm_provider: LLMProvider = LLMProvider.OLLAMA
    llm_model: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434"
    github_token: SecretStr = SecretStr("")

    # Per-agent temperatures (0.0 = deterministic, 1.0 = creative)
    temperature_research: float = 0.3
    temperature_strategy: float = 0.5
    temperature_planner: float = 0.7
    temperature_content: float = 0.8

    # Max characters of prior context passed to the content agent
    content_context_limit: int = 800

    debug: bool = False

    @model_validator(mode="after")
    def _check_provider_credentials(self) -> "Settings":
        is_github = self.llm_provider == LLMProvider.GITHUB
        if is_github and not self.github_token.get_secret_value():
            raise ValueError("GITHUB_TOKEN is required when LLM_PROVIDER=github")
        return self


settings = Settings()
