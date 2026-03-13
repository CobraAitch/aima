from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for market research, competitor info, or industry trends.

    Use this tool to find real-world data about products, markets,
    and competitors instead of relying on training data.
    """
    search = DuckDuckGoSearchResults(max_results=5)
    return search.invoke(query)
