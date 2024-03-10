from asyncio import sleep
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import TelegramAPIError, BotBlocked
from filters import IsOurChats
from loader import dp, bot
from states import SendAllMessage
from utils.db_api import quick_commands


@dp.message_handler(Command("send_all"), IsOurChats())
async def send_all(message: types.Message):
    await message.answer(f'Данная команда отправит сообщение ВСЕМ пользователям, подписаным на бота.\n'
                         f'Просьба использовать данную отправку в критичных ситуациях по ВСМ или подобных, '
                         f'требующих массового и немедленного информирования всех сотрудников\n'
                         f'Для подтверждения напиши: ТОЧНО ОТПРАВИТЬ ВСЕМ\n\n'
                         f'Отвечать сейчас и далее нужно через "Ответить" (Reply)')


@dp.message_handler(IsOurChats(), text="ТОЧНО ОТПРАВИТЬ ВСЕМ")
async def send_confim(message: types.Message):
    await message.answer(f'Напиши сообщение, которое ты хочешь отправить...\n')
    await SendAllMessage.Send.set()


@dp.message_handler(IsOurChats(), state=SendAllMessage.Send)
async def send_all_in_state(message: types.Message, state: FSMContext):
    await state.update_data(Send=message.text)
    data = await state.get_data()
    Send = data.get("Send")
    users_all = await quick_commands.select_all_users()
    await state.finish()

    count = 0
    for user in users_all:
        if user.ban != 1:
            try:
                await bot.send_message(user.chat_id, Send)
                logging.warning(f'Сообщение из массовой рассылки отправлено пользователю: {user.chat_id} | {user.name}')
            except:
                logging.warning(
                    f'Ошибка! Сообщение из массовой рассылки НЕ отправлено пользователю: {user.chat_id} | {user.name}')
                await sleep(1)
            count +=1
            if count == 5:
                count = 0
                await sleep(1)

