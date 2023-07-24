from aiogram import Router


def get_admin_router() -> Router:
    from . import (
        start,
        exit_from_menu,
        show_admins,
        show_users,
        reset_limit_requests,
    )

    router = Router()
    router.include_router(start.router)
    router.include_router(exit_from_menu.router)
    router.include_router(show_admins.router)
    router.include_router(show_users.router)
    router.include_router(reset_limit_requests.router)

    return router
