import smtplib
import ssl
import logging
from email.message import EmailMessage
from typing import Optional

from config import settings
from models import Customer, RegistrationToken

logger = logging.getLogger(__name__)


# =====================================================
# CORE EMAIL SENDER
# =====================================================

def send_email(
    *,
    to_email: str,
    subject: str,
    html_body: str,
    text_body: Optional[str] = None,
) -> None:
    """
    Verstuurt een e-mail via SMTP.
    Ondersteunt MailHog (dev) en echte SMTP (prod).
    """

    # ----------------------------------------------
    # HARD STOP indien e-mail uitgeschakeld
    # ----------------------------------------------
    if not settings.WEBSITE_EMAIL_ENABLED:
        logger.warning("E-mail verzending is uitgeschakeld (WEBSITE_EMAIL_ENABLED=false)")
        return

    msg = EmailMessage()
    msg["From"] = settings.WEBSITE_EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    if text_body:
        msg.set_content(text_body)
        msg.add_alternative(html_body, subtype="html")
    else:
        msg.set_content(html_body, subtype="html")

    smtp_host = settings.WEBSITE_SMTP_HOST
    smtp_port = int(settings.WEBSITE_SMTP_PORT)
    smtp_user = settings.WEBSITE_SMTP_USERNAME or None
    smtp_password = settings.WEBSITE_SMTP_PASSWORD or None
    use_tls = settings.WEBSITE_SMTP_TLS

    logger.info(
        "Sending email to=%s host=%s port=%s tls=%s",
        to_email,
        smtp_host,
        smtp_port,
        use_tls,
    )

    try:
        if use_tls:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.starttls(context=context)
                if smtp_user:
                    server.login(smtp_user, smtp_password)
                server.send_message(msg)
        else:
            # MailHog / plain SMTP
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                if smtp_user:
                    server.login(smtp_user, smtp_password)
                server.send_message(msg)

        logger.info("E-mail succesvol verzonden naar %s", to_email)

    except Exception as exc:
        logger.exception("E-mail verzending mislukt")
        raise RuntimeError(f"Failed to send email: {exc}") from exc


# =====================================================
# REGISTRATION / PASSWORD SETUP EMAIL
# =====================================================

def send_registration_email(
    *,
    customer: Customer,
    token: RegistrationToken,
) -> None:
    """
    Stuurt registratie / password-setup e-mail.
    """

    base_url = settings.PUBLIC_APP_BASE_URL.rstrip("/")

    # 👉 CONSISTENT met frontend + swagger
    setup_url = f"{base_url}/password-setup?token={token.token}"

    subject = "Voltooi je registratie bij Casuse"

    text_body = f"""\
Hallo {customer.first_name},

Welkom bij Casuse.

Klik op onderstaande link om je wachtwoord in te stellen
en je account te activeren:

{setup_url}

Deze link is tijdelijk geldig.

Met vriendelijke groet,
Casuse
"""

    html_body = f"""\
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Registratie Casuse</title>
</head>
<body>
    <p>Hallo <strong>{customer.first_name}</strong>,</p>

    <p>Welkom bij <strong>Casuse</strong>.</p>

    <p>
        Klik op onderstaande knop om je wachtwoord in te stellen
        en je account te activeren:
    </p>

    <p>
        <a href="{setup_url}"
           style="
               display:inline-block;
               padding:12px 20px;
               background-color:#1e40af;
               color:#ffffff;
               text-decoration:none;
               border-radius:6px;
               font-weight:bold;
           ">
            Wachtwoord instellen
        </a>
    </p>

    <p>
        Of kopieer deze link:<br>
        <a href="{setup_url}">{setup_url}</a>
    </p>

    <p>Deze link is tijdelijk geldig.</p>

    <p>
        Met vriendelijke groet,<br>
        <strong>Casuse</strong>
    </p>
</body>
</html>
"""

    send_email(
        to_email=customer.email,
        subject=subject,
        html_body=html_body,
        text_body=text_body,
    )
