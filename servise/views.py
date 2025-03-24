import re
from pprint import pformat

from database.connection import engine, add_db
from database.table_diagrams import User, UserRole, Token

from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse


from log.logger import logger
from passlib.context import CryptContext
from email_validator import validate_email
from servise.token import create_access_tokens, create_refresh_tokens

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

        user_data = {"user_id": add_user.id, "user_email": add_user.email}
        access = await create_access_tokens(user_data)
        refresh = await create_refresh_tokens(user_data)
        add_token = Token(user_id=add_user.id, access_token=access,  refresh_token=refresh, create_date=datetime.now())
        await add_db(db, add_token)

        # return RedirectResponse(url=" http://127.0.0.1:8080/activation?refresh=false")
        logger.info(f"Зарегистрирован новый пользователь: {confirm_user.username}, email {confirm_user.user_email}")
        return JSONResponse(status_code=200,
                            content="Пользователь успешно зарегистрирован.")
    except Exception as exc:
        logger.error(f"Получено исключение при исполнении кода {exc}")
        return JSONResponse(status_code=500, content="Ошибка: Не удались зарегистрировать пользователя.")


async def user_login(user, db):
    try:
        user_data = db.query(User).filter(User.email == user.email).first()
        if user_data:
            verify_password = pwd_context.verify(user.password, user_data.password)
            if verify_password:
                user_token = db.query(Token).filter(Token.user_id == user_data.id).first()
                logger.info(f"Успешная авторизация пользователя: {user.email}")
                return JSONResponse(status_code=200, content={"access_token": user_token.access_token, "refresh_token": user_token.refresh_token})
            else:
                logger.error(f"Попытка авторизации пользователя под данными: login - {user.email} password - {user.password}")
                return JSONResponse(status_code=401, content="Ошибка: Логин или пароль не верны.")
        else:
            logger.error(f"Попытка авторизации пользователя под данными: login - {user.email} password - {user.password}")
            return JSONResponse(status_code=401, content="Ошибка: Логин или пароль не верны.")
    except Exception as exc:
        logger.error(f"Получено исключение при исполнении кода {exc}")
        return JSONResponse(status_code=500, content="Ошибка: Не удались авторизоваться.")
