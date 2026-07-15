from google import genai

from app.config import settings


class GeminiService:
    """
    Wrapper around Google's Gemini models.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.text_model = settings.GEMINI_TEXT_MODEL
        self.vision_model = settings.GEMINI_VISION_MODEL

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.models.generate_content(
            model=self.text_model,
            contents=prompt
        )

        return response.text


gemini = GeminiService()