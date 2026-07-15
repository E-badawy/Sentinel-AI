from app.services.web_search import web_search


class NewsService:

    def get_ai_news(self):

        results = web_search.search(
            "Latest Artificial Intelligence news today",
            max_results=5
        )

        articles = []

        for item in results:

            articles.append(
                f"""
Title:
{item['title']}

URL:
{item['url']}

Summary:
{item['body']}
"""
            )

        return "\n".join(articles)


news_service = NewsService()