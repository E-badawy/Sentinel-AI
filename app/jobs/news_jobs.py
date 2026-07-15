from app.services.news_service import news_service
from app.whatsapp.sender import whatsapp_sender
from app.agents.sentinel import agent
from app.services.llm import llm
from app.utils.logger import logger
import traceback


def send_ai_news(phone_number: str):

    try:
        print("Running scheduled job...")

        search_results = news_service.get_ai_news()

        print("Search completed.")

        # Prevent sending extremely large prompts to the LLM
        search_results = search_results[:5000]

        summary = llm.chat(
            prompt=f"""
            You are an AI news editor.

            Below are today's AI news articles.

            Write a concise daily briefing.

            Requirements:
            - Maximum 250 words.
            - Use bullet points.
            - Highlight only the most important stories.
            - End with one sentence explaining why today's news matters.

            News:

            {search_results}
            """
            )

        print("Summary length:", len(summary))

        summary = summary[:3500]
        
        print("LLM completed.")

        response = whatsapp_sender.send_text(
            to=phone_number,
            message=summary
        )

        print("WhatsApp Response:")
        print(response)

    except Exception as e:
        print("=" * 60)
        print("SCHEDULER FAILED")
        logger.exception("FAILED SCHEDULER")
        traceback.print_exc()
        print("=" * 60)