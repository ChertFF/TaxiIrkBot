from time import gmtime, strftime

import emoji

from data import config
from aiogram import types
from aiogram.dispatcher.filters import Command
from filters import IsOurChats
from loader import dp, bot
from utils.misc.logging import filename


@dp.message_handler(Command("logs_out"), IsOurChats())
async def logs_out(message: types.Message):
    await message.answer("Выгружаю для тебя логи...")
    await bot.send_document(config.ADMIN_CHAT_ID, types.InputFile(filename), caption=f'Актуальные данные для тебя {emoji.emojize(":heart_hands:")}')