import os
from dotenv import load_dotenv

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time


from database.connection import Base

load_dotenv()

class UserRole(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    number = Column(String)
    number_active = Column(Boolean, nullable=False, default=False)
    create_date = Column(Time, nullable=False)
    update_date = Column(Time)
    blocking = Column(Boolean, nullable=False, default=False)
    blocking_data = Column(Time)
    role = Column(Integer, ForeignKey("user_role.id"))

class Token(Base):
    __tablename__ = 'user_token_access'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    create_date = Column(Time, nullable=False)
    update_date = Column(Time)
