from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from nutrilog.config import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.database_url)
    session_maker = async_sessionmaker(engine)
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
