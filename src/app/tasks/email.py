from src.app.core.tkq import broker
from src.app.core.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib


@broker.task
async def send_email(
    email_to: str,
    subject: str,
    body: str
) -> None:
    """Отправка email через SMTP."""
    message = MIMEMultipart()
    message["From"] = settings.smtp.user
    message["To"] = email_to
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    await aiosmtplib.send(
        message,
        hostname=settings.smtp.host,
        port=settings.smtp.port,
        username=settings.smtp.user,
        password=settings.smtp.password
    )

