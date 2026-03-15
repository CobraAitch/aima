import logging
from typing import cast

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from aima.agents.state import CampaignState
from aima.config import CampaignStatus, settings
from aima.llm.factory import create_llm
from aima.models.content import GeneratedContent

log = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a creative content specialist. Generate ready-to-publish "
    "marketing content.\n"
    "You MUST populate ALL of the following fields:\n"
    "- social_media_posts: list of 3 posts, each with platform "
    "(Instagram/LinkedIn/Twitter), post_type, text, hashtags (list), "
    "cta (call to action)\n"
    "- ad_copies: list of 2 ads, each with headline, body, cta, "
    "target_audience\n"
    "- email_subject_lines: list of 5 compelling email subjects\n"
    "- key_talking_points: list of 5 key talking points\n"
    "Keep posts concise, platform-specific, and engaging."
)

MAX_RETRIES = 2


def _truncate(text: str, limit: int | None = None) -> str:
    """Word-boundary truncation so we don't blow up prompt length."""
    if limit is None:
        limit = settings.content_context_limit
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)
    return (cut[0] if len(cut) > 1 else text[:limit]) + "..."


def create_content(state: CampaignState) -> dict[str, object]:
    """Generates platform-specific marketing content."""
    brief = state["brief"]
    research = state.get("research")
    strategy = state.get("strategy")

    prompt = (
        f"Product: {brief.product}\n"
        f"Goal: {brief.goal}\n"
        f"Market: {brief.market}\n\n"
    )

    if research:
        research_text = (
            f"Overview: {research.market_overview}\n"
            f"Trends: {', '.join(research.trends)}"
        )
        prompt += f"Research:\n{_truncate(research_text)}\n\n"

    if strategy:
        strategy_text = (
            f"Positioning: {strategy.positioning}\n"
            f"Value Proposition: {strategy.value_proposition}"
        )
        prompt += f"Strategy:\n{_truncate(strategy_text)}\n\n"

    prompt += (
        "Generate:\n"
        "- 3 social media posts (Instagram, LinkedIn, Twitter)\n"
        "- 2 ad copies\n"
        "- 5 email subject lines\n"
        "- 5 key talking points"
    )

    log.info("generating content for %s", brief.product)

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            llm = create_llm(temperature=settings.temperature_content)
            structured_llm = llm.with_structured_output(GeneratedContent)
            content = cast(GeneratedContent, structured_llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]))
            return {
                "content": content,
                "status": CampaignStatus.COMPLETED,
                "messages": [AIMessage(
                    content=f"Content done: {len(content.social_media_posts)} posts, "
                            f"{len(content.ad_copies)} ads"
                )],
            }
        except Exception as exc:
            last_error = exc
            log.warning("content attempt %d/%d failed: %s", attempt, MAX_RETRIES, exc)

    msg = f"Content agent failed after {MAX_RETRIES} attempts"
    raise RuntimeError(msg) from last_error
