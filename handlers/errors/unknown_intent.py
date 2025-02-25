import logging
from aiogram_dialog import DialogManager

from utils import send_message

USER_ERROR_INFO = "Ваша прошлая сессия оказалась недействительной. Пожалуйста, введите команду /start ещё раз"


async def on_unknown_intent(event, dialog_manager: DialogManager):
    logging.info("Restarting dialog: %s", event.exception)
    await send_message(chat_id=event.update.callback_query.message.chat.id, text=USER_ERROR_INFO)
