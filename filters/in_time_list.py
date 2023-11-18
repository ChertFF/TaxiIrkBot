from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from data.config import TIME_LIST


class InTimeList(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text in [time[0] for time in TIME_LIST]
