import logging

import emoji
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove

from data import config
from filters import IsPrivate
from loader import bot, dp
from aiogram import types
from utils.db_api import quick_commands
from utils.notify_admins import second_send_notify_admins


@dp.message_handler(IsPrivate(), text="Отменить утреннюю доставку")
async def cansel_order(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    if user.second_ordered == 1:
        await user.update(second_ordered=0).apply()
        await message.answer(f'Ты успешно отказался от утренней доставки! {emoji.emojize(":check_mark:")}', reply_markup=ReplyKeyboardRemove())
        logging.warning( f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} отказался от утренней доставки | {user.name},{user.second_city} {user.second_address}, {user.number}, {user.second_time} | Отказ от доставки | {message.text}')
        await second_send_notify_admins(dp, message, user, "Отказ от утренней доставки")
    else:
        await message.answer(f'Увы, но я тебя не помню, ты не записывался в утреннюю доставку {emoji.emojize(":thinking_face:")}\n', reply_markup=ReplyKeyboardRemove())
        logging.warning( f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} пытался отказаться от утренней доставки | {user.name}, {user.second_address}, {user.number}, {user.second_time} | Отказ от доставки | {message.text}')
