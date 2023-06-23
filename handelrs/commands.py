from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from DataBase import TelegramUsers
from fastools import close_state

async def command_start(message: types.Message, state: FSMContext):
    #Function from Fastools, if state is exists close him & if bot remember message, delete him
    await close_state(state=state, chat_id=message.chat.id)
    #Send welcome-message
    await message.answer(f"Hello, {message.from_user.first_name}!")
    #Check, is user exists
    if not await TelegramUsers.exists(TelegramID=message.from_user.id):
        #Create new User in DB
        await TelegramUsers.create(TelegramID=message.from_user.id, first_name=message.from_user.first_name)


#Register hadlers
def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, state='*')