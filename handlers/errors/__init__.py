from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent

from .unknown_intent import on_unknown_intent

router = Router()

router.errors.register(
    on_unknown_intent,
    ExceptionTypeFilter(UnknownIntent)
)
