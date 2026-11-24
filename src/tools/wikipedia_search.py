# Wikipedia search tool for general background information

from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper


# Initialise Wikipedia with up to three results
wiki_api = WikipediaAPIWrapper(
    top_k_results=3,
    doc_content_chars_max=1500
)


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for general knowledge and background information.

    Use this tool for definitions, historical context,
    scientific concepts and established factual information.
    """

    return wiki_api.run(query)