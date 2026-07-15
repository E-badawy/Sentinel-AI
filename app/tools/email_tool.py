from app.services.email_service import email_service
from app.services.extractor_service import extractor_service
from app.memory.pending_actions import pending_actions


class EmailTool:

    EMAIL_SCHEMA = """
    {
    "recipient": "",
    "subject": "",
    "body": ""
    }
    """

    def execute(
        self,
        message: str,
        session_id: str
    ) -> str:

        data = extractor_service.extract(
            message=message,
            schema=self.EMAIL_SCHEMA
        )

        recipient = data.get("recipient", "")
        subject = data.get("subject", "")
        body = data.get("body", "")

        if not recipient:
            return "I couldn't determine the recipient."

        if not subject:
            subject = "Sent from Sentinel AI"

        if not body:
            body = "No message was provided."

        def send():

            return email_service.send_email(
                recipient=recipient,
                subject=subject,
                body=body
            )

        pending_actions.set(
            session_id,
            {
                "type": "email",
                "callback": send
            }
        )

        return f"""
    📧 Email ready to send.

    To: {recipient}

    Subject: {subject}

    Reply YES to send.

    Reply NO to cancel.
    """


email_tool = EmailTool()