from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from src.config import Config
from src.db.models import User, Frequency, Bouquet, Subscription

engine = create_async_engine(
    Config.DATABASE_URL,
    echo=False,
    future=True
)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

async def initdb():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)