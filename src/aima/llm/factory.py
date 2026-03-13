from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama

from aima.config import settings

def create_llm(
        temperature: float | None = None,
        max_tokens: int | None = None,
) -> BaseChatModel:
    match settings.llm_provider:
        case "ollama":
            return ChatOllama(
                model=settings.llm_model,
                base_url=settings.ollama_base_url,
                temperature=temperature,
                num_predict=max_tokens,
            )
        case "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model_name=settings.llm_model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        case "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model_name=settings.llm_model,
                temperature=temperature,
                max_tokens=max_tokens,
                max_retries=2,
            )
        case "github":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=settings.llm_model,
                base_url="https://models.github.ai/inference",
                api_key=settings.github_token,
            )
        case _:
            raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")