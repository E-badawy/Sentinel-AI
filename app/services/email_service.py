import smtplib
from email.message import EmailMessage

from app.config import settings


class EmailService:

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str
    ) -> str:

        message = EmailMessage()

        message["From"] = settings.EMAIL_ADDRESS
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP(
            settings.EMAIL_SMTP_SERVER,
            settings.EMAIL_SMTP_PORT
        ) as smtp:

            smtp.starttls()

            smtp.login(
                settings.EMAIL_ADDRESS,
                settings.EMAIL_APP_PASSWORD
            )

            smtp.send_message(message)

        return "Email sent successfully."


email_service = EmailService()