from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from data.config import CITY_LIST
from utils.db_api import quick_commands


class InCityList(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        for i in range(len(CITY_LIST)):
            for j in range(len(CITY_LIST[i])):
                if CITY_LIST[i][j] == message.text:
                    return True
        return False
