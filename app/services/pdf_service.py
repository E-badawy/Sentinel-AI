import fitz


class PDFService:

    def extract_text(
        self,
        filepath: str
    ) -> str:

        document = fitz.open(filepath)

        text = ""

        for page in document:

            text += page.get_text()

        document.close()

        return text


pdf_service = PDFService()