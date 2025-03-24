import os
import smtplib
import urllib.parse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime, timedelta

from log.logger import logger
from servise.token import create_access_tokens, create_registr_token



async def send_email(password_hash, user_email, name):
    """
    Отправка сообщения пользователю
    """
    msg = MIMEMultipart()
    msg['From'] = os.getenv("MAIL_SERVICE_USER")
    msg['To'] = user_email

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    msg['Subject'] = "Подтверждение регистрации."
    email_body = "<p>Для подтверждения регистрации перейдите по ссылке: <br><a href='confirmation_link'>Подтвердить регистрацию</a><br><p>"
    new_access_token = create_registr_token(
        data={"username": name,
              "user_email": user_email,
              "password_hash": password_hash},
        expires_delta=access_token_expires)
    encoded_params = urllib.parse.urlencode({'data': new_access_token})
    final_url = f"{os.getenv("URL_CONFIRM")}?{encoded_params}"
    msg.attach(MIMEText(email_body.replace("confirmation_link", final_url), 'html'))

    try:
        with smtplib.SMTP(os.getenv("MAIL_SERVICE_ADRESS"), int(os.getenv("MAIL_SERVICE_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("MAIL_SERVICE_USER"), os.getenv("MAIL_SERVICE_PASS"))
            server.send_message(msg)
            logger.info(f"Письмо успешно отправлено на {user_email}")
            return True
    except Exception as e:
        logger.info(f'Произошла ошибка при отправке письма: {e}')
        return False