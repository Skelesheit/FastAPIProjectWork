register_subject = "Подтвердите вашу почту"
invite_subject = "Вас пригласили как сотрудника в компанию"


def generate_register_html(confirm_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Подтверждение регистрации</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 24px;
            }}
            .header {{
                font-size: 20px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 16px;
            }}
            .text {{
                font-size: 16px;
                color: #555555;
                margin-bottom: 24px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #2196F3;
                color: #ffffff !important;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            .footer {{
                font-size: 12px;
                color: #999999;
                margin-top: 40px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Подтверждение регистрации</div>
            <div class="text">
                Здравствуйте! Пожалуйста, подтвердите свою почту, нажав на кнопку ниже.
            </div>
            <a class="button" href="{confirm_url}">Подтвердить почту</a>
            <div class="footer">
                Если вы не регистрировались — просто проигнорируйте это письмо.
            </div>
        </div>
    </body>
    </html>
    """


def generate_invite_html(confirm_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Приглашение в компанию</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 24px;
            }}
            .header {{
                font-size: 20px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 16px;
            }}
            .text {{
                font-size: 16px;
                color: #555555;
                margin-bottom: 24px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #4CAF50;
                color: #ffffff !important;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            .footer {{
                font-size: 12px;
                color: #999999;
                margin-top: 40px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Вас пригласили присоединиться к компании</div>
            <div class="text">
                Для присоединения нажмите на кнопку ниже. Ссылка действует в течение 24 часов.
            </div>
            <a class="button" href="{confirm_url}">Присоединиться</a>
            <div class="footer">
                Если вы не ожидали это письмо, просто проигнорируйте его.
            </div>
        </div>
    </body>
    </html>
    """
