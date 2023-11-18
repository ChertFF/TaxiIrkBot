import asyncio
import logging

import emoji
from aiogram.dispatcher.filters import Command, Text
from data import config
from filters import IsPrivate
from loader import dp, bot
from aiogram import types

from utils.db_api import quick_commands

import aiogram.utils.markdown as fmt


async def third_sept(message):
    await message.answer(f"{fmt.hitalic('Я календарь переверну - и снова третье сентября')}\n")
    await asyncio.sleep(2)
    await message.answer(f"{fmt.hitalic('На фото я твоё взгляну - и снова третье сентября')}\n")
    await asyncio.sleep(2)
    await message.answer(f"{fmt.hitalic('Но почему, но почему расстаться всё же нам пришлось?')}\n")
    gif = open('utils/media/3_sept.gif', 'rb')
    await bot.send_animation(message.chat.id, gif)


async def beats_latecomers(message):
    gif = open('utils/media/beats_latecomers.gif', 'rb')
    await bot.send_animation(message.chat.id, gif)


async def its_time_to_order_dostavka(chat_id, Send):
    gif = open('utils/media/its_time_to_order_dostavka.gif', 'rb')
    await bot.send_animation(chat_id, gif, caption=Send)


async def wow(message):
    gif = open('utils/media/wow.gif', 'rb')
    await bot.send_animation(message.chat.id, gif)
