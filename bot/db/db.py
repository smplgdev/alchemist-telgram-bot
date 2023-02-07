from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine as _create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


def create_session_maker(engine: AsyncEngine = None) -> sessionmaker:
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

