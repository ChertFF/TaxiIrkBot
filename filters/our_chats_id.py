from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data import config


class IsOurChats(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.id == config.ADMIN_CHAT_ID
