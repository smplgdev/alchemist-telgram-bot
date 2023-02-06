from aiogram import Bot
from aiogram.types import BotCommand

bot_commands = {
    "start": "Главное меню"
}


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        BotCommand(command=k, description=v)
        for k, v in bot_commands.items()
    ])
