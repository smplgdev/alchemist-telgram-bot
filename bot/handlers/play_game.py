from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from db.queries import elements_commands, game_commands
from keyboards import inline_kb
from keyboards.inline_kb import GameCallback
from services import strings
from states.game import GameStates

router = Router()


async def initialize_game(message: types.Message, session_maker: sessionmaker):
    game = await game_commands.init(
        session_maker,
        message.from_user.id
    )
    elements = await elements_commands.get_user_unlocked_elements(
        session_maker=session_maker,
        game_id=game.id,
        category_id=None
    )
    markup = inline_kb.get_user_elements_keyboard(
        game_id=game.id,
        elements=elements,
        elements_category_id=None,
        first_picked_element_id=None,
        page=1
    )
    await message.answer(
        strings.PLAY_MENU,
        reply_markup=markup
    )


async def game_handler(call: types.CallbackQuery, callback_data: GameCallback, session_maker: sessionmaker):
    game_id = callback_data.game_id
    elements_category_id = callback_data.elements_category_id
    first_element_id = callback_data.first_element_id
    second_element_id = callback_data.second_element_id
    if second_element_id and first_element_id:
        new_element = await elements_commands.check_if_recipe_exists(
            session_maker,
            elements_ids=[
                first_element_id,
                second_element_id
            ]
        )
        if new_element:
            is_not_opened = await elements_commands.add_new_unlocked_element(
                session_maker=session_maker,
                game_id=game_id,
                element_id=new_element.id
            )
            if is_not_opened:
                await call.answer(
                    strings.YOU_OPENED_NEW_ELEMENT.format(
                        element_title=new_element.title_ru
                    ),
                    show_alert=True
                )
            else:
                await call.answer(
                    strings.IT_ALREADY_OPENED.format(
                        element_title=new_element.title_ru
                    )
                )
        else:
            await call.answer(
                strings.ELEMENT_NOT_EXIST
            )
        first_element_id = None

    elements = await elements_commands.get_user_unlocked_elements(
        session_maker=session_maker,
        game_id=game_id,
        category_id=elements_category_id
    )
    markup = inline_kb.get_user_elements_keyboard(
        game_id=game_id,
        elements=elements,
        elements_category_id=elements_category_id,
        first_picked_element_id=first_element_id
    )

    await call.message.edit_reply_markup(
        reply_markup=markup
    )


async def first_element_handler(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    element = await elements_commands.find_by_title(
        session_maker,
        message.text
    )
    await state.update_data(first_element_id=element.id)
    await state.set_state(GameStates.choose_second_element)


async def second_element_handler(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    element = await elements_commands.find_by_title(
        session_maker,
        message.text
    )
    data = await state.get_data()
    elements_ids = [data.get("first_element_id"), element.id]
    new_element = await elements_commands.check_if_recipe_exists(
        session_maker,
        elements_ids
    )
    if new_element:
        await message.answer("Вы открыли: %s!" % new_element.title_ru)
    await state.set_state(GameStates.choose_first_element)


router.message.register(initialize_game, F.text == strings.PLAY_BUTTON)
router.message.register(initialize_game, Command("play"))
router.callback_query.register(game_handler, GameCallback.filter())
