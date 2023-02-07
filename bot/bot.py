import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from aioredis import Redis
from sqlalchemy import URL

from db.base import BaseModel
from db.db import create_async_engine, proceed_schemas, create_session_maker
from handlers import start
from services.set_bot_commands import set_bot_commands
from config import config

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
    await proceed_schemas(async_engine, BaseModel.metadata)

    redis = Redis(
        host=config.REDIS_IP,
        port=6379
    )
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)
    dp.include_router(start.router)

    logging.info("Starting bot...")
    try:
        await dp.start_polling(bot, session_maker=session_maker)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
