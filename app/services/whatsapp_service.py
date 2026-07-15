import os
import requests

from app.config import settings


class WhatsAppService:

    BASE_URL = "https://graph.facebook.com/v23.0"

    def get_media_url(
        self,
        media_id: str
    ):

        response = requests.get(
            f"{self.BASE_URL}/{media_id}",
            headers={
                "Authorization":
                f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
            }
        )

        response.raise_for_status()

        return response.json()["url"]

    def download_media(
        self,
        media_url: str,
        filepath: str
        ):

        response = requests.get(
            media_url,
            headers={
            "Authorization":
            f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
        }
        )

        response.raise_for_status()

        os.makedirs(
            os.path.dirname(filepath),
            exist_ok=True
        )

        with open(filepath, "wb") as file:
            file.write(response.content)

        return filepath
    
whatsapp_service = WhatsAppService()