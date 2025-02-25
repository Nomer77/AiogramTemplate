from aiogram import Router

from .commands import router as commands_router
from .errors import router as error_router

router = Router()

router.include_routers(
    error_router,
    commands_router,
)
