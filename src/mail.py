from pathlib import Path
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config

BASE_DIR = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,  
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,      
    MAIL_SSL_TLS=False,      
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,     
)

mail = FastMail(mail_config)


def create_message(
    recipients: list[str],
    subject: str,
    body: str,
    subtype: MessageType = MessageType.html,
) -> MessageSchema:
    return MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=subtype,
    )
