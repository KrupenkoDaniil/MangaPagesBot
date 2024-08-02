from aiogram.fsm.state import StatesGroup, State


class Init(StatesGroup):
    init = State()
    new_manga = State()

class Menu(StatesGroup):
    menu = State()
    new_manga = State()
    loading_page = State()
