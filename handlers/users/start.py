import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsPrivate
from loader import dp
from utils.db_api import quick_commands
import emoji

from utils.notify_admins import send_notify_admins_by_start


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await quick_commands.select_user(message.from_user.id)
        if user.chat_id == message.from_user.id:
            await message.answer("Привет, ты уже зарегистрирован!\n")
            logging.warning(f'Зарегистрированный пользователь {message.from_user.id} выбрал /start')
    except Exception:
        await quick_commands.add_user(chat_id=message.from_user.id, name=None, address=None, number=None, time=None,
                                      ordered=None)

        await message.answer(f'Привет, {message.from_user.full_name}! {emoji.emojize(":hand_with_fingers_splayed:")}\n'
                             f'Я создан для того, чтобы после работы ты с комфортом добрался до дома. \n\n'
                             f'Давай познакомимься поближе. Пройди небольшую регистрацию по команде /register')
        logging.warning(f'Пользователь {message.from_user.id} выбрал /start и зарегистрировался')
        await send_notify_admins_by_start(dp, message)

