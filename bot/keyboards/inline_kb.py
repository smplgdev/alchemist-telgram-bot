from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

from db.models.elements import Element


class GameCallback(CallbackData, prefix="game"):
    game_id: int
    elements_category_id: int | None
    first_element_id: Optional[int]
    second_element_id: Optional[int]


def get_user_elements_keyboard(
        game_id: int,
        elements: list[Element],
        elements_category_id: int | None,
        first_picked_element_id: int = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for element in elements:
        button_text = f"🟢 {element.title_ru}" \
                        if first_picked_element_id == element.id \
                        else element.title_ru
        builder.button(
            text=button_text,
            callback_data=GameCallback(
                game_id=game_id,
                elements_category_id=elements_category_id,
                first_element_id=first_picked_element_id
                if first_picked_element_id
                else element.id,
                second_element_id=element.id
                if first_picked_element_id
                else None
            )
        )
    builder.adjust(1)
    return builder.as_markup()
