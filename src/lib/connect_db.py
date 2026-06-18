from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

URL_DB = os.environ.get("DB")

engine = create_async_engine(
    URL_DB,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def db():
    async with SessionLocal() as session:
        yield session
