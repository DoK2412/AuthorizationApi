from pydantic import BaseModel
from fastapi import Query

class Registration(BaseModel):
    name: str = Query(description='Имя пользователя')
    password: str = Query(description='Пароль пользователя')
    confirmPassword: str = Query(description='Подтверждение пароля пользователя')
    email: str = Query(description="Электронная почта пользователя")

class ConfirmRegistration(BaseModel):
    username: str = Query(description='Имя пользователя')
    password_hash: str = Query(description='Пароль пользователя')
    user_email: str = Query(description="Электронная почта пользователя")

class Login(BaseModel):
    email: str = Query(description='Имя пользователя')
    password: str = Query(description='Пароль пользователя')