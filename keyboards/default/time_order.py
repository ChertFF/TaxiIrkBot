from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import TIME_LIST, MORNING_TIME_LIST

select_time = ReplyKeyboardMarkup(TIME_LIST, resize_keyboard=True)

select_second_time = ReplyKeyboardMarkup(MORNING_TIME_LIST, resize_keyboard=True)