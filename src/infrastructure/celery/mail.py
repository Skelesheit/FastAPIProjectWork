import smtplib
from email.message import EmailMessage

from celery import shared_task

from config import settings


def _send_email_sync(to: str, subject: str, body: str, subtype: str = "html"):
    msg = EmailMessage()
    msg["From"] = settings.mail_username
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body, subtype=subtype)

    if settings.MAIL_USE_TLS:  # SMTPS (465)
        with smtplib.SMTP_SSL(settings.MAIL_SERVER, settings.MAIL_PORT) as s:
            s.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            s.send_message(msg)
    else:  # STARTTLS (587)
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as s:
            s.ehlo()
            if settings.MAIL_START_TLS:
                s.starttls()
                s.ehlo()
            s.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            s.send_message(msg)


@shared_task(
    name="mail.send",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
    ignore_result=True,
)
def send_email_message(payload: dict) -> None:
    _send_email_sync(
        to=payload["to"],
        subject=payload["subject"],
        body=payload["body"],
        subtype=payload.get("subtype", "html"),
    )
