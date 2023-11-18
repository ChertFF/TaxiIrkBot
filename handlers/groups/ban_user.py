import emoji
from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsOurChats
from loader import dp, bot
from utils.db_api import quick_commands


@dp.message_handler(Command("ban"), IsOurChats())
async def ban(message: types.Message):
    if message.get_args() == "":
        await message.answer(f'Ошибка! Не указан ID пользователя')
    else:
        args = int(message.get_args())
        user = await quick_commands.select_user(args)
        try:
            await user.update(ban=1).apply()
            await message.answer(f'Пользователь с ID {user.chat_id} был заблокирован')
            await bot.send_message(args, f'Увы, запись в доставку более недоступна.\n'
                                         f'Обратись к своему руководителю!\n'
                                         f'ID блокировки: {user.chat_id}')
        except:
            await message.answer(f'Ошибка! Неверно введен ID пользователя')


@dp.message_handler(Command("sban"), IsOurChats())
async def ban(message: types.Message):
    if message.get_args() == "":
        await message.answer(f'Ошибка! Не указан ID пользователя')
    else:
        args = int(message.get_args())
        user = await quick_commands.select_user(args)
        try:
            await user.update(ban=1).apply()
            await message.answer(f'Пользователь с ID {user.chat_id} был заблокирован')
        except:
            await message.answer(f'Ошибка! Неверно введен ID пользователя')


@dp.message_handler(Command("unban"), IsOurChats())
async def ban(message: types.Message):
    if message.get_args() == "":
        await message.answer(f'Ошибка! Не указан ID пользователя')
    else:
        args = int(message.get_args())
        user = await quick_commands.select_user(args)
        try:
            await user.update(ban=0).apply()
            await message.answer(f'Пользователь с ID {user.chat_id} был разблокирован')
        except:
            await message.answer(f'Ошибка! Неверно введен ID пользователя')
