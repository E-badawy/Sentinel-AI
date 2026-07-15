from ddgs import DDGS
import trafilatura


class WebSearchService:

    def search(
        self,
        query: str,
        max_results: int = 5
    ):

        results = []

        with DDGS() as ddgs:

            search_results = list(
                ddgs.text(
                    query,
                    max_results=max_results
                )
            )

        for item in search_results:

            results.append({
            "title": item.get("title", ""),
            "url": item.get("href", ""),
            "body": item.get("body") or item.get("snippet", "")
            })

        return results

    def scrape(
        self,
        url: str
    ):

        downloaded = trafilatura.fetch_url(url)

        if not downloaded:
            return ""

        text = trafilatura.extract(downloaded)

        return text or ""


web_search = WebSearchService()