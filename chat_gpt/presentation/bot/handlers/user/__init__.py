from aiogram import Router


def get_user_router() -> Router:
    from . import info, start, text_query, voice_query

    router = Router()

    router.include_router(info.router)
    router.include_router(start.router)
    router.include_router(text_query.router)
    router.include_router(voice_query.router)

    return router
