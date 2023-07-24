from aiogram.fsm.state import StatesGroup, State


class ShowUsers(StatesGroup):
    main = State()
    user_info = State()
    add_user = State()
