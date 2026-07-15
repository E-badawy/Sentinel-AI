from app.services.ga4_service import ga4_service
from app.services.llm import llm


class AnalyticsTool:

    def execute(
        self,
        question: str
    ):

        data = ga4_service.visitors_last_7_days()

        prompt = f"""
        You are a website analytics expert.

        Analytics Data:

        {data}

        User Question:

        {question}

        Answer naturally.
        """

        return llm.chat(prompt)


analytics_tool = AnalyticsTool()