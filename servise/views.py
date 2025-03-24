import re

from sqlalchemy.orm import Session
from database.connection import engine, add_db
from database.table_diagrams import User, UserRole

from database.connection import SessionLocal


from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse


from log.logger import logger
from passlib.context import CryptContext
from email_validator import validate_email

from servise.client_message import send_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authorization(register, db):
    user = db.query(User).filter(User.email == register.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Ошибка: Пользователь уже зарегистрирован."
        )
    if re.match( r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$', register.password) is None:
        raise HTTPException(
            status_code=400,
            detail="Ошибка: пароль не соответствует стандарту."
        )
    if register.password != register.confirmPassword:
        raise HTTPException(
            status_code=400,
            detail="Ошибка: Введенные пароли не совпадают."
        )
    try:
        validate_email(register.email)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Ошибка: Не удалось определить email пользователя."
        )

    password_hash = pwd_context.hash(register.password)
    send_message = await send_email(password_hash, register.email, register.name)
    if send_message:
        return JSONResponse(status_code=200, content="Письмо подтверждение регистрации успешно отправлено. Если письма нет во входящих, проверьте спам.")
    else:
        return JSONResponse(status_code=400, content="Не удалось отправить письмо подтверждения регистрации, повторите позже.")

async def confirm_registration_user(confirm_user, db):
    try:
        role = db.query(UserRole).filter(UserRole.type == "user").first()
        add_user = User(name=confirm_user.username, password=confirm_user.password_hash,  email=confirm_user.user_email, active=True, create_date=datetime.now(), role=role.id)
        await add_db(db, add_user)
        # return RedirectResponse(url=" http://127.0.0.1:8080/activation?refresh=false")
        logger.info(f"Зарегистрирован новый пользователь: {confirm_user.username}, email {confirm_user.user_email}")
        return JSONResponse(status_code=200,
                            content="Пользователь успешно зарегистрирован.")
    except Exception as exc:
        logger.error(f"Получено исключение при исполнении кода {exc}")
        return JSONResponse(status_code=500, content="Ошибка: Не удались зарегистрировать пользователя.")

