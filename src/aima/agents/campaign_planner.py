import logging
from typing import cast

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from aima.agents.state import CampaignState
from aima.config import CampaignStatus, settings
from aima.llm.factory import create_llm
from aima.models.campaign import CampaignPlan

log = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a senior campaign planner. Create a detailed campaign plan.\n"
    "You MUST populate ALL of the following fields:\n"
    "- campaign_name: a catchy campaign name\n"
    "- summary: 2-3 sentence campaign summary\n"
    "- audience_segments: list of 2+ segments, each with name, "
    "age_range (format: '25-34'), interests (list), platforms (list)\n"
    "- channels: list of 2+ channels, each with channel name, "
    "objective, budget_pct (0-100), key_actions (list)\n"
    "- key_messages: list of 3+ key marketing messages\n"
    "- timeline_weeks: campaign duration in weeks (integer)"
)

MAX_RETRIES = 2


def plan_campaign(state: CampaignState) -> dict[str, object]:
    """Generates a structured campaign plan from all prior context."""
    brief = state["brief"]
    research = state.get("research")
    strategy = state.get("strategy")

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
            f"Trends: {', '.join(research.trends)}\n\n"
        )

    if strategy:
        prompt += (
            f"Marketing Strategy:\n"
            f"Positioning: {strategy.positioning}\n"
            f"Value Proposition: {strategy.value_proposition}\n"
            f"Budget Recommendation: ${strategy.total_budget_recommendation:,.0f}\n\n"
        )

    prompt += "Create a detailed campaign plan based on all available data."

    log.info("planning campaign for %s", brief.product)

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            llm = create_llm(temperature=settings.temperature_planner)
            structured_llm = llm.with_structured_output(CampaignPlan)
            plan = cast(CampaignPlan, structured_llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]))
            return {
                "plan": plan,
                "status": CampaignStatus.PLANNED,
                "messages": [AIMessage(content=f"Plan ready: {plan.campaign_name}")],
            }
        except Exception as exc:
            last_error = exc
            log.warning("planner attempt %d/%d failed: %s", attempt, MAX_RETRIES, exc)

    msg = f"Planner agent failed after {MAX_RETRIES} attempts"
    raise RuntimeError(msg) from last_error
