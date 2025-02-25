from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from handlers.filters import IsUserNotBanned, IsPersonalDialog, IsUserAdmin
from orm.models.users import TelegramUser

router = Router()


async def command_start(message: types.Message, state: FSMContext):
    if not await TelegramUser.exists(TelegramID=message.from_user.id):
        await TelegramUser.create(TelegramID=message.from_user.id, first_name=message.from_user.first_name)

    if await state.get_state() is not None:
        await state.clear()

    await message.answer(
        f"{message.from_user.first_name}, Добро пожаловать!"
    )


async def command_whoami(message: types.Message):
    await message.answer(
        f"TelegramID: {message.from_user.id}\n"
        f"Your first_name: {message.from_user.first_name}\n"
        f"Your last_name: {message.from_user.last_name}\n"
        f"This chat_id: {message.chat.id}"
    )


async def command_give_ban(message: types.Message):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Используйте: /give_ban {telegram_user_id}")
        return

    telegram_user_id = int(args[1])
    user = await TelegramUser.get_or_none(TelegramID=telegram_user_id)
    if not user:
        await message.answer("Пользователь не найден.")
        return

    user.is_banned = True
    await user.save()
    await message.answer(f"Пользователь {telegram_user_id} был забанен.")


async def command_give_admin(message: types.Message):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Используйте: /give_admin {telegram_user_id}")
        return

    telegram_user_id = int(args[1])
    user = await TelegramUser.get_or_none(TelegramID=telegram_user_id)
    if not user:
        await message.answer("Пользователь не найден.")
        return

    user.is_admin = True
    await user.save()
    await message.answer(f"Пользователь {telegram_user_id} теперь администратор.")


async def command_help(message: types.Message):
    help_text = (
        "Список доступных команд:\n"
        "- /give_ban {telegram_user_id} - Забанить пользователя (только для админом)\n"
        "- /give_admin {telegram_user_id} - Назначить пользователя администратором (только для админом)\n"
        "- /whoami - Получить информацию о себе (доступно всем)"
    )
    await message.answer(help_text)


router.message.register(command_start, IsUserNotBanned(), IsPersonalDialog(), Command("start"), StateFilter("*"))
router.message.register(command_whoami, IsUserNotBanned(), Command("whoami"), StateFilter("*"))
router.message.register(command_give_ban, IsUserAdmin(), IsPersonalDialog(), Command("give_ban"), StateFilter("*"))
router.message.register(command_give_admin, IsUserAdmin(), IsPersonalDialog(), Command("give_admin"), StateFilter("*"))
router.message.register(command_help, IsUserAdmin(), IsPersonalDialog(), Command("help"), StateFilter("*"))
