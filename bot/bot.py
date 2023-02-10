import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import Redis
from sqlalchemy import URL

from config import config
from create_elements import create_elements
from db.base import BaseModel
from db.db import create_async_engine, create_session_maker, delete_schemas, proceed_schemas
from handlers import start, play_game
from services.set_bot_commands import set_bot_commands

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(),
    parse_mode='HTML'
)


postgres_url = URL.create(
    "postgresql+asyncpg",
    username=config.DB_USERNAME,
    password=config.DB_PASSWORD,
    host=config.DB_IP,
    database=config.DB_NAME,
    port=5432
)


async def main():
    await set_bot_commands(bot)

    async_engine = create_async_engine(postgres_url)
    session_maker = create_session_maker(async_engine)
    await delete_schemas(engine=async_engine, metadata=BaseModel.metadata)
    await proceed_schemas(engine=async_engine, metadata=BaseModel.metadata)
    await create_elements(session_maker)

    redis = Redis(
        host=config.REDIS_IP,
        port=6379
    )
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage, session_maker=session_maker)
    dp.include_router(start.router)
    dp.include_router(play_game.router)

    logging.info("Starting bot...")
    try:
        await dp.start_polling(bot, session_maker=session_maker)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
