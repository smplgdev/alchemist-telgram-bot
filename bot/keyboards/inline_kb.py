import math
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models.elements import Element


class GameCallback(CallbackData, prefix="game"):
    game_id: int
    elements_category_id: int | None
    page: int
    first_element_id: Optional[int]
    second_element_id: Optional[int]


class PaginationCallback(CallbackData, prefix="pagination"):
    action: str
    page: int


PAGE_LIMIT = 14


def get_user_elements_keyboard(
        game_id: int,
        elements: list[Element],
        elements_category_id: int | None,
        first_picked_element_id: int = None,
        page: int = 1
) -> InlineKeyboardMarkup:
    max_page = math.ceil(len(elements) / PAGE_LIMIT)
    builder = InlineKeyboardBuilder()
    count_buttons = 0
    for element in elements[(page-1)*PAGE_LIMIT:page*PAGE_LIMIT]:
        button_text = f"🟢 {element.title_ru}" \
                        if first_picked_element_id == element.id \
                        else element.title_ru
        builder.button(
            text=button_text,
            callback_data=GameCallback(
                game_id=game_id,
                elements_category_id=elements_category_id,
                page=page,
                first_element_id=first_picked_element_id
                if first_picked_element_id
                else element.id,
                second_element_id=element.id
                if first_picked_element_id
                else None
            )
        )
        count_buttons += 1

    builder.button(
        text="<<",
        callback_data=PaginationCallback(
            action="prev_page",
            page=page-1
            if page != 1
            else max_page
        )
    ),
    builder.button(
        text=f"{page}/{max_page}",
        callback_data=PaginationCallback(
            action=" ",
            page=page
        )
    ),
    builder.button(
        text=">>",
        callback_data=PaginationCallback(
            action="next_page",
            page=page + 1
            if page != 1
            else 1
        )
    )
    elements_rows = math.floor(count_buttons/2)
    elements_rows_list = [2 for _ in range(elements_rows)] + ([1] if count_buttons % 2 else [])
    rows = [*elements_rows_list, 3]
    builder.adjust(*rows)
    return builder.as_markup()
