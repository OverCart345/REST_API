import redis.asyncio as aioredis
from sqlmodel import create_engine, Session, SQLModel
from core.config import settings
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass


def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


async def get_redis_client() -> aioredis.Redis:
    client = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", 
        encoding="utf-8", 
        decode_responses=True
    )
    return client
