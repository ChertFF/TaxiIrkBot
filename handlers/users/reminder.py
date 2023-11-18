from asyncio import sleep
import logging
import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsOurChats, IsPrivate
from loader import dp, bot
from utils.db_api import quick_commands


@dp.message_handler(Command("remind_me"), IsPrivate())
async def remind_me(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    remind_status = user.reminder
    if remind_status == 1:
        remind_status = "включены"
    else:
        remind_status = "выключены"
    await message.answer(
        f'Данная команда поможет тебе не забыть записаться в доставку!  {emoji.emojize(":alarm_clock:")}\n'
        f'Бот будет отправлять тебе напоминание каждый день в 15:00 о том, что нужно подумать, как ты доберешься до дома вечером.\n\n'
        f''
        f'Статус уведомлений: {remind_status}\n\n'
        f'/remind_on - включить уведомления\n'
        f'/remind_off - выключить уведомления\n')
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} нажал /remind_me  | {message.text}')


@dp.message_handler(Command("remind_on"), IsPrivate())
async def remind_me(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    await user.update(reminder=1).apply()
    await message.answer(
        f'Готово! Бот будет напоминать тебе в 15:00, чтобы ты не забыл записаться в доставку {emoji.emojize(":three_o’clock:")}')
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} включил напоминания | {message.text}')


@dp.message_handler(Command("remind_off"), IsPrivate())
async def remind_me(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    await user.update(reminder=0).apply()
    await message.answer(
        f'Готово!Уведомления о необходимости записи в доставку выключены {emoji.emojize(":cross_mark:")}')
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} выключил напоминания | {message.text}')
