import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from nutrilog.config import settings
from nutrilog.database.models import Base

logger = logging.getLogger()


async def migrate_tables() -> None:
    logger.info("Starting to migrate")

    print(f"Connecting to: {settings.database_url}")
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Done migrating")


if __name__ == "__main__":
    asyncio.run(migrate_tables())
