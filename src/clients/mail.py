from config import settings
from src.auth.token import generate_join_email_token, generate_access_token
from src.clients import html
from src.infrastructure.celery.mail import send_email_message


def _enqueue_email(to: str, subject: str, body: str, subtype: str = "html") -> None:
    send_email_message.delay(
        {
            "to": to,
            "subject": subject,
            "body": body,
            "subtype": subtype
        }
    )


def send_registration_email(user_id: int, email: str) -> None:
    token = generate_access_token(user_id)
    url = f"{settings.base_url}client/mail/{token}"
    _enqueue_email(
        email,
        html.register_subject,
        html.generate_register_html(url)
    )


def send_invite_email(enterprise_id: int, email: str) -> None:
    token = generate_join_email_token(enterprise_id, email)
    url = f"{settings.base_url}client/mail/join-to-enterprise/{token}"
    _enqueue_email(
        email,
        html.invite_subject,
        html.generate_invite_html(url)
    )
