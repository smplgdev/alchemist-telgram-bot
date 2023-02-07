from aiogram.fsm.state import StatesGroup, State


class GameStates(StatesGroup):
    choose_first_element = State()
    choose_second_element = State()
