from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from services import strings


def start() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text=strings.PLAY_BUTTON
    )
    builder.button(
        text=strings.STATISTICS_BUTTON
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
