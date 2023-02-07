from sqlalchemy.orm import sessionmaker

from db.models.games import Game


async def init(
        session_maker: sessionmaker,
        user_telegram_id: int,
) -> Game:
    async with session_maker() as session:
        async with session.begin():
            game = Game(
                user_telegram_id=user_telegram_id,
                unlocked_elements_ids=[1, 2, 3, 4]
            )
            await session.merge(game)
    return game
