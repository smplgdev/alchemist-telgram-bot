from aiogram import types, Router
from aiogram.filters import CommandStart

from keyboards import reply_kb
from middlewares.check_register import RegisterCheck
from services import strings

router = Router()


async def start_handler(message: types.Message):
    await message.answer(
        strings.START.format(first_name=message.from_user.first_name),
        reply_markup=reply_kb.start()
    )


router.message.register(start_handler, CommandStart())
router.message.middleware(RegisterCheck())
