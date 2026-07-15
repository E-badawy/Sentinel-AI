from tavily import TavilyClient

from app.config import settings
from app.services.web_search import web_search
from app.utils.logger import logger


class SearchService:

    def __init__(self):

        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def search(
        self,
        query: str
    ) -> str:

        output = []

        # ---------- Tavily ----------

        try:

            tavily = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=3
            )

            for item in tavily["results"]:

                content = web_search.scrape(item["url"])

                if not content:
                    content = item.get("body", "")

                output.append(
                    f"""
                    Title: {item['title']}
                    URL: {item['url']}
                    Content:
                {content[:3000]}
                """
            )

        except Exception as e:

            logger.exception("search error")

        # ---------- DuckDuckGo ----------

        try:

            results = web_search.search(
                query,
                max_results=3
            )

            for item in results:

                output.append(
                    f"""
                Title: {item['title']}
                URL: {item['url']}
                content = item.get("body", "")
                """
                )

        except Exception as e:

            logger.exception("Duck duck go URL error")

        return "\n\n".join(output)


search_service = SearchService()