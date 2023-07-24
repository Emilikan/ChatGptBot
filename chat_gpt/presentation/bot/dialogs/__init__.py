from aiogram import Dispatcher
from .show_admins import ShowAdmins  # noqa
from .show_users import ShowUsers  # noqa


def register_dialogs(dp: Dispatcher):
    from . import (
        show_admins,
        show_users,
    )

    dp.include_router(show_admins.ui)
    dp.include_router(show_users.ui)
