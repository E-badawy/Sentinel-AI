from app.services.search import search_service
from app.services.llm import llm


class SearchTool:

    def execute(self, query: str) -> str:

        search_results = search_service.search(query)

        prompt = f"""
You are Sentinel AI.

Using the search results below, answer the user's question accurately.

Search Results:
{search_results}

User Question:
{query}
"""

        return llm.chat(prompt)


search_tool = SearchTool()