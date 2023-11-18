from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import dp, bot

from utils.db_api import quick_commands
from utils.notify_admins import send_notify_admins_by_banned


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        user = await quick_commands.select_user(message.from_user.id)
        if (message.chat.type == types.ChatType.PRIVATE) and user.ban != 1:
            return True
        elif (message.chat.type == types.ChatType.PRIVATE) and user.ban == 1:
            await send_notify_admins_by_banned(dp, message)
            return False
        else:
            return False
