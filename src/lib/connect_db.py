from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

URL_DB = os.environ.get("DB")


engine = create_async_engine(URL_DB, echo=True)

creat_session = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=AsyncSession
)


async def db():
    async with creat_session() as session:
        yield session
