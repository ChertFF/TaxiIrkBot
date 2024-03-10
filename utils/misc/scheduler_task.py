import asyncio
import functools
import logging
from asyncio import sleep
import aiogram.utils.markdown as fmt
import emoji
import tabulate as tabulate
from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError, BotBlocked

from data.config import ADMIN_CHAT_ID
from handlers.groups.out_orders import out_orders
from loader import bot
from utils.db_api import quick_commands

import aioschedule

from utils.send_media import its_time_to_order_dostavka


async def reset_ordered():
    users_ordered = await quick_commands.select_orders()
    for user in users_ordered:
        await user.update(ordered=0).apply()
    logging.warning(f'Сброшены состояния заказов')

    users_ordered = await quick_commands.select_second_orders()
    for user in users_ordered:
        await user.update(second_ordered=0).apply()
    logging.warning(f'Сброшены состояния утренних заказов')


async def send_reminder():
    users_all = await quick_commands.select_reminder()
    Send = (f'По-дружески напоминаю, что пора записаться в доставку {emoji.emojize(":face_with_rolling_eyes:")}\n\n'
            f'Чтобы записаться воспользуйся командой /order\n'
            f'Чтобы выключить такие уведомления - /remind_off\n')
    for user in users_all:
        if user.ban != 1 and user.ordered != 1:
            try:
                await bot.send_message(user.chat_id, Send)
                # await its_time_to_order_dostavka(user.chat_id, Send)
                logging.warning(
                    f'Уведомление о записи в доставку отправлено пользователю: {user.chat_id} | {user.name}')
                await asyncio.sleep(0.2)
            except:
                logging.warning(
                    f'Ошибка! Уведомление о записи в доставку НЕ отправлено пользователю: {user.chat_id} | {user.name}')
                await asyncio.sleep(0.2)


async def everyday_ban():
    users_ban = await quick_commands.select_for_everyday_ban()
    message_for_admins = f"{fmt.hbold('Пользователи были заблокированы!')}\n"
    for user in users_ban:
        try:
            await user.update(ban=1).apply()
            #Линк для блокировки пользователя
            link = f"tg://user?id={user.chat_id}"
            #Добавляем каждого заблокированного пользователя к переменной
            message_for_admins += (f"{user.chat_id:*^11} | "
                                   f"{user.created_at.strftime('%d.%m.%Y %H:%M:%S')} | "
                                   f'{fmt.hlink("Тык", link)}\n')
            #Текст сообщения для пользователя
            Send = (f'Увы, запись в доставку более недоступна.\n'
                    f'Обратись к своему руководителю!\n'
                    f'ID блокировки: {user.chat_id}')
            logging.warning(f'Пользователь был заблокирован: {user.chat_id}')
            await bot.send_message(user.chat_id, Send)
            await asyncio.sleep(0.01)
        except:
            logging.warning(f'Ошибка! Пользователь был НЕ был заблокирован: {user.chat_id}')
    await bot.send_message(ADMIN_CHAT_ID, message_for_admins)


async def scheduler_reset_ordered():
    aioschedule.every().day.at("03:00").do(reset_ordered)
    aioschedule.every().day.at("15:00").do(send_reminder)
    aioschedule.every().day.at("08:30").do(everyday_ban)
    aioschedule.every().day.at("18:00").do(functools.partial(out_orders, "first"))
    aioschedule.every().day.at("22:00").do(functools.partial(out_orders, "second"))
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)

# async def scheduler_send_reminder():
#     aioschedule.every().day.at("18:25").do(send_reminder)
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(5)
