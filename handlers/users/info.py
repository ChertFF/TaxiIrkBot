import logging
import emoji
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from data import config
from filters import IsPrivate, InTimeList
from loader import dp, bot
from aiogram import types

from utils.db_api import quick_commands

import aiogram.utils.markdown as fmt


@dp.message_handler(Command("info"), IsPrivate())
async def select_time_order(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)

    order = f"Заказан {emoji.emojize('✅')}" if user.ordered == 1 else f"Не заказан {emoji.emojize('❌')}"
    morning_order = f"Заказан {emoji.emojize('✅')}" if user.second_ordered == 1 else f"Не заказан  {emoji.emojize('❌')}"
    reminder = f"Включены {emoji.emojize('✅')}" if user.reminder == 1 else f"Отключены  {emoji.emojize('❌')}"

    if user.ordered == 1:
        message_order = f"{fmt.hbold('Населенный пункт: ')} {user.city}\n"\
                        f"{fmt.hbold('Адрес: ')} {user.address}\n"\
                        f"{fmt.hbold('Время: ')} {user.time}"
    else:
        message_order = ''

    if user.second_ordered == 1:
        message_second_order = f"{fmt.hbold('Населенный пункт: ')} {user.second_city}\n"\
                               f"{fmt.hbold('Адрес: ')} {user.second_address}\n"\
                               f"{fmt.hbold('Время: ')} {user.second_time}"
    else:
        message_second_order = ''

    await message.answer(
        f"{emoji.emojize(':backhand_index_pointing_down:')} {fmt.hbold('Данные по тебе')} {emoji.emojize(':backhand_index_pointing_down:')} \n\n"
        f"{fmt.hbold('ФИО:')} {user.name}\n"
        f"{fmt.hbold('Номер телефона: ')} {user.number}\n\n"

        f"{fmt.hbold('Данные по вечерней доставке:')}\n"
        f"{fmt.hbold('Статус: ')} {order}\n"
        f"{message_order}\n\n"

        f"{fmt.hbold('Данные по утренней доставке:')}\n"
        f"{fmt.hbold('Статус: ')} {morning_order}\n"
        f"{message_second_order}\n\n"

        f"{fmt.hbold('Напоминания о доставке:')}\n"
        f"{fmt.hbold('Статус: ')} {reminder}\n"
        f"", reply_markup=ReplyKeyboardRemove())
    logging.warning(f'Пользователь {message.from_user.id} просматривает данные по себе| {message.text};{user.name}')
