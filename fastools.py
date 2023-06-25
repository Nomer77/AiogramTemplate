from aiogram.dispatcher import Dispatcher
from aiogram.utils import exceptions
from settings import bot

async def close_state(state: FSMContext, chat_id: int) -> None:
    if await state.get_state() is not None:
        await delete_message(state, chat_id)
        await state.finish()

async def delete_message(state: FSMContext, chat_id: int) -> None:
    async with state.proxy() as base:
        if 'message' in base:
            try:
                await bot.delete_message(chat_id, base['message'].message_id)
            except exceptions.MessageToDeleteNotFound:
                logging.warning("MessageToDeleteNotFound")
                logging.debug(message, "\n", await state.get_state())
            finally:
                del base['message']

async def dalek(state: FSMContext, CHAT_ID: int, MESSAGE_TEXT: str, MESSAGE_MARKUP=None, edit_message=True) -> None:
    """Удобная функция продолжающая диалог методом изменения сообщений с обработкой ошибок"""
    if await state.get_state() is None:
        return await bot.send_message(CHAT_ID, MESSAGE_TEXT, reply_markup=MESSAGE_MARKUP)
    async with state.proxy() as base:
        if not 'message' in base:
            base['message'] = await bot.send_message(CHAT_ID, MESSAGE_TEXT, reply_markup=MESSAGE_MARKUP)
            return True
        if edit_message:
            message = base['message']
    try:
        if edit_message:
            await message.edit_text(text=MESSAGE_TEXT, reply_markup=MESSAGE_MARKUP)
            return True
        raise
    except:
        await delete_message(state=state, chat_id=CHAT_ID)
        async with state.proxy() as base:
            base['message'] = await bot.send_message(CHAT_ID, MESSAGE_TEXT, reply_markup=MESSAGE_MARKUP)

async def set_message(state: FSMContext, message: types.Message) -> None:
    async with state.proxy() as base:
        base['message'] = message