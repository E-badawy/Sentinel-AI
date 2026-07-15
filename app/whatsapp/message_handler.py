import os
import uuid
from app.security.authorization import authorization_service
from app.config import settings
from app.services.whatsapp_service import whatsapp_service
from app.whatsapp.sender import whatsapp_sender
from app.agents.sentinel import agent
from app.services.transcription import transcription_service
from app.services.pdf_service import pdf_service
from app.services.data_service import data_service
from app.utils.logger import logger
from app.memory.memory_service import (
    save_memory,
    get_memories
)

def handle_text(message: dict):

    sender = message["from"]

    text = message["text"]["body"]

    if not authorization_service.is_authorized(sender):

        whatsapp_sender.send_text(
            to=sender,
            message=(
                "Sorry, you are not authorized "
                "to use Sentinel AI."
            )
        )

        return

    print(f"Incoming Text: {text}")

    # -------------------------------
    # Retrieve previous memories
    # -------------------------------

    memories = get_memories(sender)

    prompt = f"""
        Previous conversation memories:

        {memories}

        Current user message:

        {text}
        """

    response = agent.chat(
        message=prompt,
        session_id=sender
    )

    # -------------------------------
    # Save conversation
    # -------------------------------

    save_memory(
        sender,
        text
    )

   
    # -------------------------------
    # Send response
    # -------------------------------

    if isinstance(response, dict) and "file" in response:

        whatsapp_sender.send_document(
            to=sender,
            filepath=response["file"]
        )

        whatsapp_sender.send_text(
            to=sender,
            message=response["message"]
        )

    else:

        whatsapp_sender.send_text(
            to=sender,
            message=response
        )

def handle_image(message: dict):

    sender = message["from"]

    try:

        image = message["image"]

        media_id = image["id"]

        mime_type = image.get(
            "mime_type",
            "image/jpeg"
        )

        extension = mime_type.split("/")[-1]

        filename = f"{uuid.uuid4()}.{extension}"

        print(f"Incoming Image ID: {media_id}")

        media_url = whatsapp_service.get_media_url(
            media_id
        )

        filepath = os.path.join(
            settings.MEDIA_FOLDER,
            "images",
            )
        
        filepath = whatsapp_service.download_media(
            media_url,
            filepath
        )

        logger.info(f"Saved image: {filepath}")

        whatsapp_sender.send_text(
            to=sender,
            message="✅ Image downloaded successfully."
        )

    except Exception as e:

        logger.exception("Failed to render image")

        whatsapp_sender.send_text(
            to=sender,
            message="❌ Failed to download image."
        )
        
        
def handle_document(message: dict):

    sender = message["from"]

    try:

        document = message["document"]

        media_id = document["id"]

        print(f"Incoming Document: {document.get('filename', 'document.pdf')}")

        media_url = whatsapp_service.get_media_url(
            media_id
        )

        filepath = os.path.join(
            settings.MEDIA_FOLDER,
            "documents",
            document.get("filename", "document.pdf")
        )

        filepath = whatsapp_service.download_media(
            media_url,
            filepath
        )

        print(f"Saved: {filepath}")

        text = pdf_service.extract_text(
            filepath
        )

        text = text[:12000]

        response = agent.chat(
            message=f"""
                The user uploaded a PDF.

                Answer based on the document below.

                {text}
                """,
            session_id=sender
        )

        whatsapp_sender.send_text(
          to=sender,
         message=response
        )

    except Exception as e:

        logger.exception("document error")

        whatsapp_sender.send_text(
            to=sender,
            message="❌ Failed to download document."
        )
    
def handle_audio(message: dict):

    sender = message["from"]

    try:

        audio = message["audio"]

        media_id = audio["id"]

        mime_type = audio.get(
            "mime_type",
            "audio/ogg"
        )

        extension = mime_type.split("/")[-1].split(";")[0].strip()

        print(f"Incoming Audio ID: {media_id}")

        media_url = whatsapp_service.get_media_url(
            media_id
        )

        filepath = os.path.join(
            settings.MEDIA_FOLDER,
            "audio",
            f"{uuid.uuid4()}.{extension}"
        )

        filepath = whatsapp_service.download_media(
            media_url,
            filepath
        )

        print(f"Saved: {filepath}")

        transcript = transcription_service.transcribe(
            filepath
        )

        print(f"Transcript: {transcript}")

        response = agent.chat(
            message=transcript,
            session_id=sender
        )

        whatsapp_sender.send_text(
             to=sender,
             message=response
        )

    except Exception as e:

        logger.exception("audio error")

        whatsapp_sender.send_text(
            to=sender,
            message="❌ Failed to download audio."
        )
        
def handle_spreadsheet(message: dict):

    try:

        sender = message["from"]

        document = message["document"]

        media_id = document["id"]

        filename = document.get("filename", "spreadsheet.xlsx")

        print(f"Incoming Spreadsheet: {filename}")

        media_url = whatsapp_service.get_media_url(
            media_id
        )

        filepath = os.path.join(
            settings.MEDIA_FOLDER,
            "documents",
            filename
        )

        filepath = whatsapp_service.download_media(
            media_url,
            filepath
        )

        print(f"Saved: {filepath}")

        dataframe = data_service.load(
            filepath
        )

        summary = data_service.summarize(
            dataframe
        )

        response = agent.chat(
            message=f"""
        A user uploaded a spreadsheet.

        Dataset Summary

        Rows: {summary['rows']}

        Columns: {summary['columns']}

        Column Names:
        {summary['column_names']}

        Missing Values:
        {summary['missing_values']}

        First Five Rows:
        {summary['preview']}

        Numeric Statistics:
        {summary['statistics']}

        Analyze the dataset and provide:

        1. A brief overview.
        2. Data quality issues.
        3. Key insights.
        4. Interesting patterns.
        5. Recommendations.

        Limit your response to about 400 words.
        """,
        session_id=sender   
        )
        whatsapp_sender.send_text(
            to=sender,
            message=response
        )

    except Exception as e:

        logger.exception("analysis error")

        whatsapp_sender.send_text(
            to=sender,
            message="❌ Failed to analyze spreadsheet."
        )