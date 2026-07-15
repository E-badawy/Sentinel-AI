from app.services.document_service import document_service
from app.services.llm import llm


class DocumentTool:

    def execute(
        self,
        message: str
    ):

        prompt = f"""
You are a document assistant.

The user wants a document created.

User request:
{message}

Generate the content that should go inside the document.

Make it professional and well structured.
"""

        content = llm.chat(prompt)

        title = "Sentinel AI Report"

        if "pdf" in message.lower():

            filepath = document_service.generate_pdf(
                title,
                content
            )

            return {
                "message": "PDF generated successfully",
                "file": filepath
            }

        else:

            filepath = document_service.generate_docx(
                title,
                content
            )

            return {
                "message": "DOCX generated successfully",
                "file": filepath
            }


document_tool = DocumentTool()