from aiogram.filters import BaseFilter
from aiogram import types

from orm.models.users import TelegramUser


class IsUserNotBanned(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if await TelegramUser.exists(TelegramID=message.from_user.id, is_banned=True):
            return False
        return True


class IsUserAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return await TelegramUser.exists(TelegramID=message.from_user.id, is_banned=False, is_admin=True)


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str | list):
        self.chat_type = chat_type

    async def __call__(self, message: types.Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


class IsPersonalDialog(ChatTypeFilter):
    def __init__(self):
        super().__init__(["private"])
