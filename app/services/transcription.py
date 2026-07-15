from groq import Groq

from app.config import settings


class TranscriptionService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.LLM_API_KEY
        )

    def transcribe(
        self,
        audio_path: str
    ) -> str:

        with open(audio_path, "rb") as audio:

            transcription = self.client.audio.transcriptions.create(
                file=audio,
                model="whisper-large-v3"
            )

        return transcription.text


transcription_service = TranscriptionService()