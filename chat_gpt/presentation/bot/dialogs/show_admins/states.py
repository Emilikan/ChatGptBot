from aiogram.fsm.state import StatesGroup, State


class ShowAdmins(StatesGroup):
    main = State()
    admin_info = State()
    add_admin = State()
