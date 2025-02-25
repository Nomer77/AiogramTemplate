from aiogram import Router

from .welcome import dialog as welcome_dialog


router = Router()
router.include_routers(
    welcome_dialog
)
