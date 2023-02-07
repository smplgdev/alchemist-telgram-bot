from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from db.models.elements import Element
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


def get_elements_keyboard(elements: list[Element]):
    builder = ReplyKeyboardBuilder()
    for element in elements:
        builder.button(
            text=element.title_ru
        )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
