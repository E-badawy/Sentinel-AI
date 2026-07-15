import os
import mimetypes
import requests

from app.config import settings


class WhatsAppSender:

    BASE_URL = "https://graph.facebook.com/v23.0"

    def send_text(
        self,
        to: str,
        message: str
    ):

        url = (
            f"{self.BASE_URL}/"
            f"{settings.WHATSAPP_PHONE_NUMBER_ID}"
            "/messages"
        )

        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": message
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        return response.json()

    def send_document(
        self,
        to: str,
        filepath: str,
        filename: str = None
    ):

        if filename is None:
            filename = os.path.basename(filepath)

        mime_type, _ = mimetypes.guess_type(filepath)

        if mime_type is None:
            mime_type = "application/octet-stream"

        with open(filepath, "rb") as file:

            upload = requests.post(
                f"{self.BASE_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/media",
                headers={
                    "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
                },
                files={
                    "file": (
                        filename,
                        file,
                        mime_type
                    )
                },
                data={
                    "messaging_product": "whatsapp"
                }
            )

        print("Upload Status:", upload.status_code)
        print("Upload Response:", upload.text)

        upload.raise_for_status()

        media_id = upload.json()["id"]

        response = requests.post(
            f"{self.BASE_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages",
            headers={
                "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "document",
                "document": {
                    "id": media_id,
                    "filename": filename
                }
            }
        )

        print("Send Status:", response.status_code)
        print("Send Response:", response.text)

        response.raise_for_status()

        return response.json()


whatsapp_sender = WhatsAppSender()