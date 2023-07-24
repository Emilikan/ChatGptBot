from aiogram.fsm.state import StatesGroup, State


class AdminMenu(StatesGroup):
    menu = State()
    add_admin = State()
