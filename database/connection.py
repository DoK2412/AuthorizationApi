import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    os.getenv("SQLALCHEMY_DATABASE_URL")
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def add_db(db, request):
    db.add(request)
    db.commit()
    db.refresh(request)
