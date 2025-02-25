from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config

# Enable echo = true if we want SQL queries to be printed
async_engine = create_async_engine(Config.DATABASE_URL)

Session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session():
    async with Session() as session:
        yield session
