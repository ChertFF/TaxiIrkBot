import logging

import emoji
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
import aiogram.utils.markdown as fmt

from data import config
from filters import IsPrivate
from keyboards.default import select_cancel_order_kb
from loader import bot, dp
from aiogram import types
from utils.db_api import quick_commands
from utils.notify_admins import send_notify_admins


@dp.message_handler(Command("cancel"), IsPrivate())
async def select_time_order(message: types.Message):
    await message.answer(f'Подскажи, от какой доставки ты хочешь отказаться?', reply_markup=select_cancel_order_kb)


@dp.message_handler(IsPrivate(), text="Отменить вечернюю доставку")
async def cansel_order(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    if user.ordered == 1:
        await user.update(ordered=0).apply()
        await message.answer(f'Ты успешно отказался от доставки! {emoji.emojize("✅")}')
        await message.answer(f'Учитывай, что корректным считается отказ не менее чем за 2 часа до подачи машины!', reply_markup=ReplyKeyboardRemove())
        logging.warning( f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} отказался от доставки | {user.name}, {user.city}, {user.address}, {user.number}, {user.time} | Отказ от доставки | {message.text}')
        await send_notify_admins(dp, message, user, "Отказ от доставки")
    else:
        await message.answer(f'Увы, но я тебя не помню, ты не записывался в доставку {emoji.emojize("🫤")}\n', reply_markup=ReplyKeyboardRemove())
        logging.warning( f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} пытался отказаться от доставки | {user.name}, {user.city}, {user.address}, {user.number}, {user.time} | Отказ от доставки | {message.text}')
