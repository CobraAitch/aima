from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from aima.agents.state import CampaignState
from aima.llm.factory import create_llm
from aima.tools.web_search import search_web

SYSTEM_PROMPT = """You are a market research analyst with access to web search.
Use the search tool to find real data about the product, competitors,
market trends, and target demographics.
Search at least 2-3 times to gather comprehensive data.
Then synthesize your findings into a structured research report."""


def research_market(state: CampaignState) -> dict:
    """Research agent node with web search capability.

    Uses the agent pattern - the agent decides when to search
    and when it has enough data to write the report.
    """
    llm = create_llm(temperature=0.3)

    brief = state.brief
    prompt = (
        f"Research the market for: {brief.product}\n"
        f"Goal: {brief.goal}\n"
        f"Market: {brief.market}\n\n"
        f"Search for competitor analysis, market trends, and target demographics.\n"
        f"Provide a comprehensive research summary."
    )

    agent = create_agent(llm, tools=[search_web], system_prompt=SYSTEM_PROMPT)
    result = agent.invoke({
        "messages": [
            HumanMessage(content=prompt),
        ]
    })

    final_message = result["messages"][-1].content

    return {
        "research": final_message,
        "status": "researched",
        "messages": [AIMessage(content="Research complete with live web data")],
    }
