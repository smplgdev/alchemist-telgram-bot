import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from db.models.user import User


async def get(session_maker: sessionmaker, telegram_id: int) -> User | None:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                sa.select(User).where(User.telegram_id == telegram_id)
            )
            user = result.one_or_none()
    return user


async def create(
        session_maker: sessionmaker,
        **user_data
) -> User:
    async with session_maker() as session:
        async with session.begin():
            user = User(**user_data)
            await session.merge(user)
    return user


async def update(
        session_maker: sessionmaker,
        telegram_id: int,
        username: str
):
    async with session_maker() as session:
        async with session.begin():
            stmt = (
                sa.update(User).
                where(User.telegram_id == telegram_id).
                values(username=username)
            )
            await session.execute(stmt)
