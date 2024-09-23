from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


engine = create_async_engine(
    f"postgresql+asyncpg://user:user@localhost:5432/db_bots",
    echo=False,
    pool_size=1000,
)

async_session = async_sessionmaker(
    engine, autocommit=False, future=True, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
