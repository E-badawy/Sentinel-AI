from openai import OpenAI

from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT


class LLMService:
    """
    Wrapper around the configured LLM provider.
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )

        self.model = settings.LLM_MODEL

    def chat(
        self,
        prompt: str,
        history=None,
        system_prompt: str = SYSTEM_PROMPT,
    ) -> str:

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        if history:
            messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )

        return response.choices[0].message.content


llm = LLMService()