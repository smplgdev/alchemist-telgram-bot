import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from aioredis import Redis

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


async def main():
    await set_bot_commands(bot)

    redis = Redis(
        host=config.REDIS_IP,
        port=6379
    )
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)
    dp.include_router(start.router)

    logging.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
