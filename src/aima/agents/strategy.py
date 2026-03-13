from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from aima.agents.state import CampaignState
from aima.llm.factory import create_llm
from aima.models.strategy import MarketingStrategy

SYSTEM_PROMPT = """You are a senior marketing strategist.
Based on the campaign brief and market research, create a detailed
marketing strategy with channel plans, positioning, and KPIs.
Be specific about budget allocation and measurable goals."""

def create_strategy(state: CampaignState) -> dict:
    """Strategy agent node.

    Uses the brief and research data to create a concrete
    marketing strategy with channel plans and KPIs.
    """
    llm = create_llm(temperature=0.5)
    structured_llm = llm.with_structured_output(MarketingStrategy)

    brief = state.brief
    prompt = (
        f"Product: {brief. product}\n"
        f"Goal: {brief. goal}\n"
        f"Market: {brief. market}\n"
        f"Budget: {brief. budget or 'Not specified'}\n\n"
        f"Market Research:\n{state.research}\n\n"
        f"Create a marketing strategy based on this research."
    )

    strategy = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])

    return {
        "strategy": strategy.model_dump_json(),
        "status": "strategized",
        "messages": [AIMessage(content=f"Strategy created: {strategy.positioning}")],
    }
