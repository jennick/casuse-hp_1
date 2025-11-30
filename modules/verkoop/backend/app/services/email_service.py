import logging
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Standaard e-mail service.
    Werkt in development zonder SMTP (console output),
    en gebruikt SMTP in productie als SMTP_HOST is ingevuld.
    """

    @staticmethod
    def send_password_reset_email(to_email: str, reset_link: str) -> None:
        subject = "Wachtwoord resetten"
        body = f"""
Beste,

Je vroeg om je wachtwoord te resetten.
Klik op onderstaande link om een nieuw wachtwoord in te stellen:

{reset_link}

Deze link is 24 uur geldig.

Met vriendelijke groeten,
Casuse Team
"""

        # SMTP geconfigureerd? → versturen
        if settings.SMTP_HOST:
            try:
                msg = MIMEMultipart()
                msg["From"] = settings.SMTP_FROM_EMAIL
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                    server.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())

                logger.info(f"[MAIL VERZONDEN] → {to_email}")
            except Exception as e:
                logger.error(f"[MAIL ERROR] {e}")
        else:
            # DEVELOPMENT: log alleen
            logger.info("=== [DEV MODE] Email service ===")
            logger.info(f"To: {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Body:\n{body}")
            logger.info("================================")
