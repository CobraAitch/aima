import logging
from typing import cast

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from aima.agents.state import CampaignState
from aima.config import CampaignStatus, settings
from aima.llm.factory import create_llm
from aima.models.strategy import MarketingStrategy

log = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a senior marketing strategist. Create a marketing strategy.\n"
    "You MUST populate ALL of the following fields:\n"
    "- positioning: one clear positioning statement\n"
    "- value_proposition: the core value proposition\n"
    "- channel_plans: list of 2+ channels, each with channel name, "
    "objective, tactics (list), kpis (list), and budget_pct (0-100)\n"
    "- timeline_weeks: campaign duration in weeks (integer)\n"
    "- total_budget_recommendation: recommended budget as a number"
)

MAX_RETRIES = 2


def create_strategy(state: CampaignState) -> dict[str, object]:
    """Builds a marketing strategy from brief + research data."""
    brief = state["brief"]
    research = state.get("research")

    prompt = (
        f"Product: {brief.product}\n"
        f"Goal: {brief.goal}\n"
        f"Market: {brief.market}\n"
        f"Budget: {brief.format_budget()}\n\n"
    )

    if research:
        prompt += (
            f"Market Research:\n"
            f"Overview: {research.market_overview}\n"
            f"Demographics: {', '.join(research.target_demographics)}\n"
            f"Trends: {', '.join(research.trends)}\n"
            f"Opportunities: {', '.join(research.opportunities)}\n\n"
        )

    prompt += "Create a marketing strategy based on this research."

    log.info("creating strategy for %s", brief.product)

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            llm = create_llm(temperature=settings.temperature_strategy)
            structured_llm = llm.with_structured_output(MarketingStrategy)
            strategy = cast(MarketingStrategy, structured_llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]))
            return {
                "strategy": strategy,
                "status": CampaignStatus.STRATEGIZED,
                "messages": [AIMessage(
                    content=f"Strategy ready: {strategy.positioning}"
                )],
            }
        except Exception as exc:
            last_error = exc
            log.warning("strategy attempt %d/%d failed: %s", attempt, MAX_RETRIES, exc)

    msg = f"Strategy agent failed after {MAX_RETRIES} attempts"
    raise RuntimeError(msg) from last_error
