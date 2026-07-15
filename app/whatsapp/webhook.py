from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from app.utils.logger import logger
from app.config import settings
from app.database.database import SessionLocal
from app.whatsapp.deduplication import is_duplicate
from app.whatsapp.message_handler import (
    handle_text,
    handle_image,
    handle_document,
    handle_spreadsheet,
    handle_audio,
)

import traceback


router = APIRouter()


# --------------------------------------------------
# Webhook Verification
# --------------------------------------------------

@router.get("/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if (
        mode == "subscribe"
        and token == settings.WHATSAPP_VERIFY_TOKEN
    ):
        return PlainTextResponse(challenge)

    return PlainTextResponse(
        "Verification failed.",
        status_code=403,
    )


# --------------------------------------------------
# Incoming Messages
# --------------------------------------------------

@router.post("/webhook")
async def receive_message(request: Request):

    try:

        body = await request.json()

        print("\n========== NEW WEBHOOK ==========")
        print(body)
        print("=================================\n")

        value = (
            body.get("entry", [{}])[0]
            .get("changes", [{}])[0]
            .get("value", {})
        )

        # Ignore delivery/read/status events
        if "messages" not in value:
            return {"status": "ignored"}

        message = value["messages"][0]

        print(f"Message ID: {message.get('id')}")
        print(f"Message Type: {message.get('type')}")
        print(f"From: {message.get('from')}")

        # -----------------------------------------
        # Deduplication
        # -----------------------------------------

        db = SessionLocal()

        try:

            if is_duplicate(message["id"], db):

                logger.warning("Duplicate message ignored.")

                return {
                    "status": "duplicate"
                }

        finally:

            db.close()

        # -----------------------------------------
        # Route by message type
        # -----------------------------------------

        message_type = message.get("type")

        if message_type == "text":

            handle_text(message)

        elif message_type == "image":

            handle_image(message)

        elif message_type == "audio":

            handle_audio(message)

        elif message_type == "document":

            filename = (
                message["document"]
                .get("filename", "")
                .lower()
            )

            if filename.endswith(
                (
                    ".csv",
                    ".xlsx",
                    ".xls",
                )
            ):

                handle_spreadsheet(message)

            else:

                handle_document(message)

        else:

            print(
                f"Unsupported message type: {message_type}"
            )

        return {
            "status": "received"
        }

    except Exception:

        print("\n========== WEBHOOK ERROR ==========")
        traceback.print_exc()
        print("===================================\n")

        # Always acknowledge the webhook so
        # WhatsApp doesn't keep retrying.
        return {
            "status": "error_handled"
        }