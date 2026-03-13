from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {"env_file": ".env"}

    llm_provider: str = "ollama"
    llm_model: str = "llama3.1:8b"
    ollama_base_url: str = "http://localhost:11434"
    github_token: str = ""

    database_url: str = "postgresql+asyncpg://aima:aima@localhost:5432/aima"

    debug: bool = False

settings = Settings()
