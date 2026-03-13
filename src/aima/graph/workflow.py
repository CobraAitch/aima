from langgraph.graph import StateGraph, START, END

from aima.agents.campaign_planner import plan_campaign
from aima.agents.content_creator import create_content
from aima.agents.research import research_market
from aima.agents.strategy import create_strategy
from aima.agents.state import CampaignState

def build_graph() -> StateGraph:
    """Build the multi-agent campaign workflow.

    Flow: START -> research -> strategy -> planner -> content -> END

    Each agent reads from and writes to the shared CampaignState.
    Research informs strategy, strategy informs the final plan.
    """
    graph = StateGraph(CampaignState)

    graph.add_node("research", research_market)
    graph.add_node("strategy", create_strategy)
    graph.add_node("planner", plan_campaign)
    graph.add_node("content", create_content)

    graph.add_edge(START, "research")
    graph.add_edge("research", "strategy")
    graph.add_edge("strategy", "planner")
    graph.add_edge("planner", "content")
    graph.add_edge("content", END)

    return graph.compile()
