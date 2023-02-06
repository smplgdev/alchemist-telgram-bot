from aiogram import types, Router
from aiogram.filters import Command

from services import message_texts

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        message_texts.START
                     .format(first_name=message.from_user.first_name)
    )
