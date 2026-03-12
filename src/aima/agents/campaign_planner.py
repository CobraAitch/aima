from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from aima.agents.state import CampaignState
from aima.llm.factory import create_llm
from aima.models.campaign import CampaignPlan

SYSTEM_PROMPT = """You are a senior marketing strategist.
Given a campaign brief, create a detailed campaign plan.
Be specific about audience segments, channels, and timeline."""

def plan_campaign(state: CampaignState) -> dict:
    """Campaign planner agent node.

    Reads the brief from state, generates a structured campaign plan,
    and writes it back to state.

    This is a LangGraph node function - it receives the full graph state
    and returns a partial state update (only the fields it changes).
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#nodes
    """
    llm = create_llm(temperature=0.7)
    structured_llm = llm.with_structured_output(CampaignPlan)

    brief = state.brief
    prompt = (
        f"Product: {brief.product}\n"
        f"Goal: {brief.goal}\n"
        f"Market: {brief.market}\n"
        f"Budget: {brief.budget or 'Not specified'}\n"
    )

    plan = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])

    return {
        "plan": plan,
        "status": "planned",
        "messages": [AIMessage(content=f"Campaign plan created: {plan.campaign_name}")]
    }