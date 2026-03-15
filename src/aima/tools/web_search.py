import logging

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool

log = logging.getLogger(__name__)

_ddg = DuckDuckGoSearchResults(num_results=5)


@tool
def search_web(query: str) -> str:
    """Search the web for market research, competitor info, or industry trends."""
    log.info("web search: %s", query)
    try:
        result: str = _ddg.invoke(query)
        return result
    except Exception:
        log.exception("search failed for query: %s", query)
        return f"Search unavailable for: {query}"
