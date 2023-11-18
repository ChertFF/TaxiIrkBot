from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import CITY_LIST

select_city = ReplyKeyboardMarkup(CITY_LIST, resize_keyboard=True)