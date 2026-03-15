import logging
from typing import Any, cast

from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from pydantic import SecretStr

from aima.config import LLMProvider, settings

log = logging.getLogger(__name__)


def create_llm(
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> BaseChatModel:
    """Build an LLM instance based on the configured provider.

    Optional deps (langchain-openai, langchain-anthropic) are imported
    lazily so the project works with just ollama installed.
    """
    provider = settings.llm_provider
    log.debug("creating llm: provider=%s model=%s", provider, settings.llm_model)

    common: dict[str, Any] = {"temperature": temperature, "max_tokens": max_tokens}

    match provider:
        case LLMProvider.OLLAMA:
            return ChatOllama(
                model=settings.llm_model,
                base_url=settings.ollama_base_url,
                num_predict=common.pop("max_tokens"),
                **common,
            )

        case LLMProvider.OPENAI:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(model=settings.llm_model, **common)

        case LLMProvider.ANTHROPIC:
            from langchain_anthropic import ChatAnthropic  # type: ignore[import-not-found]  # noqa: I001

            common["max_tokens"] = common["max_tokens"] or 4096
            return cast(
                BaseChatModel,
                ChatAnthropic(model_name=settings.llm_model, **common),
            )

        case LLMProvider.GITHUB:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=settings.llm_model,
                base_url="https://models.github.ai/inference",
                api_key=SecretStr(settings.github_token.get_secret_value()),
                **common,
            )

        case _:
            raise ValueError(f"unsupported LLM provider: {provider!r}")
