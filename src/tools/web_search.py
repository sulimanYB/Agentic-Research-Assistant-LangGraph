# Web search tool using Tavily

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from src.config import TAVILY_API_KEY

# Initialise the Tavily search integration
tavily = TavilySearch(
    max_results=5,
    tavily_api_key=TAVILY_API_KEY
)


@tool
def web_search(query: str) -> str:
    """
    Search the web for current information.

    Use this tool for recent research developments,
    general information and topics outside PubMed.
    """
    return str(tavily.invoke({"query": query}))