import logging

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from aima.agents.campaign_planner import plan_campaign
from aima.agents.content_creator import create_content
from aima.agents.research import research_market
from aima.agents.state import CampaignState
from aima.agents.strategy import create_strategy

log = logging.getLogger(__name__)


def build_graph() -> CompiledStateGraph:  # type: ignore[type-arg]
    """Assembles the multi-agent campaign workflow.

    Pipeline: research -> strategy -> planner -> content

    Each node reads from shared CampaignState and returns a
    partial state update. Research feeds strategy, strategy
    feeds the planner, planner feeds content generation.
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

    log.info("workflow graph compiled")
    return graph.compile()
