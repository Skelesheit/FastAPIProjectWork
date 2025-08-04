from email.message import EmailMessage

from aiosmtplib import send

from config import settings
from src.auth.token import generate_join_email_token, generate_access_token
from src.clients import html


async def send_email_message(msg: EmailMessage) -> None:
    await send(
        msg,
        hostname=settings.MAIL_SERVER,
        start_tls=settings.MAIL_START_TLS,
        use_tls=settings.MAIL_USE_TLS,
        port=settings.MAIL_PORT,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD,
    )


def generate_message(email: str, subject: str, body: str, subtype="html") -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = settings.MAIL_USERNAME
    msg["To"] = email
    msg["Subject"] = subject
    msg.set_content(body, subtype=subtype)
    return msg


async def send_registration_email(user_id: int, email: str) -> None:
    token = generate_access_token(user_id)
    url = f"{settings.BASE_URL}client/mail/{token}"
    html_content = html.generate_register_html(url)
    msg = generate_message(email, html.register_subject, html_content)
    await send_email_message(msg)


async def send_invite_email(enterprise_id: int, email: str) -> None:
    member_token = generate_join_email_token(enterprise_id, email)
    url = f"{settings.BASE_URL}client/mail/join-to-enterprise/{member_token}"
    html_content = html.generate_invite_html(url)
    msg = generate_message(email, html.invite_subject, html_content)
    await send_email_message(msg)
