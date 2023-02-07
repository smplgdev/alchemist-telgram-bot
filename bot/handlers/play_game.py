from aiogram import Router, types, F
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from db.queries import game_commands, elements_commands
from keyboards import reply_kb
from services import strings
from states.game import GameStates

router = Router()


async def initialize_game(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    game = await game_commands.init(
        session_maker,
        message.from_user.id
    )
    print(game)
    await state.set_state(GameStates.choose_first_element)
    elements_ids = game.unlocked_elements_ids
    elements = await elements_commands.get_elements(session_maker, elements_ids)
    markup = reply_kb.get_elements_keyboard(elements)
    await message.answer(
        strings.PLAY_MENU,
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
router.message.register(first_element_handler, F.state == GameStates.choose_first_element)
router.message.register(second_element_handler, F.state == GameStates.choose_second_element)
