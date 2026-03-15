import logging
from typing import cast

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from aima.agents.state import CampaignState
from aima.config import CampaignStatus, settings
from aima.llm.factory import create_llm
from aima.models.research import MarketResearch
from aima.tools.web_search import search_web

log = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a market research analyst. Use the search_web tool to gather "
    "real data, then produce a structured research report.\n\n"
    "Steps:\n"
    "1. Search for the product/brand and its market position\n"
    "2. Search for competitors and their strengths/weaknesses\n"
    "3. Search for current industry trends\n"
    "4. Synthesize your findings into the structured report\n\n"
    "You MUST populate ALL of the following fields:\n"
    "- market_overview: 2-3 sentence overview of the market landscape\n"
    "- target_demographics: list of 3+ demographic groups (e.g. "
    "'professionals aged 25-40', 'tech-savvy millennials')\n"
    "- competitors: list of 2+ competitors, each with name, "
    "strengths (list), and weaknesses (list)\n"
    "- trends: list of 3+ current market trends\n"
    "- opportunities: list of 2+ market opportunities"
)

MAX_RETRIES = 2


def research_market(state: CampaignState) -> dict[str, object]:
    """Runs a ReAct agent that searches the web, then returns structured research."""
    brief = state["brief"]

    log.info("starting research for %s in %s", brief.product, brief.market)

    prompt = (
        f"Research the market for: {brief.product}\n"
        f"Goal: {brief.goal}\n"
        f"Market: {brief.market}\n\n"
        "Use the search_web tool to gather real market data, competitor info, "
        "and industry trends. Make multiple searches to build a complete picture."
    )

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            llm = create_llm(temperature=settings.temperature_research)
            agent = create_agent(
                model=llm,
                tools=[search_web],
                system_prompt=SYSTEM_PROMPT,
                response_format=MarketResearch,
            )
            result = agent.invoke({"messages": [HumanMessage(content=prompt)]})

            structured = result.get("structured_response")
            if structured is None:
                msg = "ReAct agent returned no structured response"
                raise RuntimeError(msg)

            research = cast(MarketResearch, structured)
            log.info(
                "research done: %d competitors, %d trends",
                len(research.competitors),
                len(research.trends),
            )
            return {
                "research": research,
                "status": CampaignStatus.RESEARCHED,
                "messages": [AIMessage(content="Market research complete")],
            }
        except Exception as exc:
            last_error = exc
            log.warning("research attempt %d/%d failed: %s", attempt, MAX_RETRIES, exc)

    msg = f"Research agent failed after {MAX_RETRIES} attempts"
    raise RuntimeError(msg) from last_error
