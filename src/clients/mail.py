from email.message import EmailMessage

from aiosmtplib import send

from config import settings
from src.auth.token import generate_access_token

subject = "Подтвердите вашу почту"


def generate_html(confirm_url: str) -> str:
    return f"""
        <p>Здравствуйте!</p>
        <p>Пожалуйста, подтвердите свою почту, перейдя по ссылке:</p>
        <p><a href="{confirm_url}">Подтвердить</a></p>
        <p>Если вы не регистрировались — просто проигнорируйте это письмо.</p>
        """


async def send_registration_email(user_id: int, email: str) -> None:
    token = generate_access_token(user_id)
    html = generate_html(f"{settings.BASE_URL}client/mail/{token}")
    print(f"token is: {token}")
    msg = EmailMessage()
    msg["From"] = settings.MAIL_USERNAME
    msg["To"] = email
    msg["Subject"] = subject
    msg.set_content(html, subtype="html")
    await send(
        msg,
        hostname=settings.MAIL_SERVER,
        start_tls=settings.MAIL_START_TLS,
        use_tls=settings.MAIL_USE_TLS,
        port=settings.MAIL_PORT,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD,
    )
