from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from aima.agents.campaign_planner import SYSTEM_PROMPT
from aima.agents.state import CampaignState
from aima.llm.factory import create_llm
from aima.models.research import MarketResearch

SYSTEM_PROMPT = """You are a market research analyst.
Analyze the market for the given product and provide structured research
including competitors, trends, demographics, and opportunities.
Be specific and data-driven in your analysis."""

def research_market(state: CampaignState) -> dict:
    """Research agent node.

    Analyzes the market based on the campaign brief and writes
    structured research data to state for downstream agents.
    """
    llm = create_llm(temperature=0.3)
    structured_llm = llm.with_structured_output(MarketResearch)

    brief = state.brief
    prompt = (
        f"Product: {brief.product}\n"
        f"Goal: {brief.goal}\n"
        f"Market: {brief.market}\n"
        f"Provide detailed market research for this product."
    )

    research = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])

    return {
        "research": research.model_dump_json(),
        "status": "researched",
        "messages": [AIMessage(content=f"Research complete: {len(research.competitors)} competitors analyzed")],
    }
