from langchain_core.tools import tool
from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """
    Search the web for up-to-date information.

    Use this tool whenever the user asks about:
    - Latest news
    - Current events
    - Sports results
    - Weather
    - Stock prices
    - Cryptocurrency
    - Recent releases
    - Information that changes over time
    """

    result = client.search(query=query, max_results=5,search_depth="advanced")

    answers = []

    for r in result["results"]:
        answers.append(
            f"{r['title']}\n"
            f"{r['content']}\n"
            f"Source: {r['url']}\n"
        )

    return "\n\n".join(answers)