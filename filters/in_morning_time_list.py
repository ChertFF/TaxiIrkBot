from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from data.config import MORNING_TIME_LIST


class InMorningTimeList(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text in [time[0] for time in MORNING_TIME_LIST]
