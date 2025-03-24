import jwt
import os
from datetime import datetime, timedelta


from dotenv import load_dotenv

load_dotenv()


async def create_access_tokens(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, os.getenv("AUTH_JWT_KEY"), algorithm=os.getenv("ALGORITHM"))


async def create_access_argo_tokens(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(days=int(os.getenv("ACCESS_TOKEN_ARGO_EXPIRE_DAYS")))
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, os.getenv("AUTH_JWT_KEY"), algorithm=os.getenv("ALGORITHM"))


async def create_refresh_tokens(data: dict):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, os.getenv("AUTH_JWT_KEY"), algorithm=os.getenv("ALGORITHM"))


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("AUTH_JWT_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload, True
    except jwt.ExpiredSignatureError:
        return None, False
    except Exception:
        return None, False


async def refresh_token(old_refresh_token: str):
    payload, is_valid = await verify_token(old_refresh_token)
    if not is_valid:
        return None, "Refresh token expired or invalid"
    access_token = await create_access_tokens(data=payload)
    refresh_token = await create_refresh_tokens(data=payload)

    return access_token, refresh_token


def create_registr_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        # если срок есть используем его
        expire = datetime.utcnow() + expires_delta
    else:
        # если нет создаем на 10 минут
        expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("AUTH_JWT_KEY"), algorithm=os.getenv("ALGORITHM"))