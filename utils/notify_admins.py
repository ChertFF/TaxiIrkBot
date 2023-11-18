import logging
from data import config
from aiogram import Dispatcher
from aiogram import Bot
from data.config import ADMINS
import aiogram.utils.markdown as fmt


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")
            await dp.bot.send_message(config.ADMIN_CHAT_ID,"Бот Запущен")

        except Exception as err:
            logging.exception(err)


async def send_notify_admins(dp: Dispatcher, message, user, text_notify):
    await dp.bot.send_message(chat_id=config.ADMIN_CHAT_ID, text=(
                           f'{fmt.hbold(text_notify)}:\n'
                           f'{fmt.hcode(user.time)};{fmt.hcode(user.name)};{fmt.hcode(user.city)};{fmt.hcode(user.address)};{fmt.hcode(user.number)}\n'
                           f'Отправил: {fmt.hlink(message.from_user.full_name, message.from_user.url)} | @{message.from_user.username}'))


async def second_send_notify_admins(dp: Dispatcher, message, user, text_notify):
    await dp.bot.send_message(chat_id=config.ADMIN_CHAT_ID, text=(
                           f'{fmt.hbold(text_notify)}:\n'
                           f'{fmt.hcode(user.second_time)};{fmt.hcode(user.name)};{fmt.hcode(user.second_city)};{fmt.hcode(user.second_address)};{fmt.hcode(user.number)}\n'
                           f'Отправил: {fmt.hlink(message.from_user.full_name, message.from_user.url)} | @{message.from_user.username}'))


async def send_notify_admins_by_start(dp: Dispatcher, message):
    await dp.bot.send_message(chat_id=config.ADMIN_CHAT_ID, text=(
                           f'{fmt.hbold("Зарегистрирован новый пользователь!")}\n'
                           f'Отправил: {fmt.hlink(message.from_user.full_name, message.from_user.url)} | @{message.from_user.username}'))


async def send_notify_admins_by_banned(dp: Dispatcher, message):
    unban = "/unban "+str(message.from_user.id)
    await dp.bot.send_message(chat_id=config.ADMIN_CHAT_ID, text=(
                           f'{fmt.hbold("Заблокированный пользователь пишет!")}\n'
                           f'Текст: {message.text}\n'
                           f'Отправил: {fmt.hlink(message.from_user.full_name, message.from_user.url)} | @{message.from_user.username}\n\n'
                           f'Разблокировать: {fmt.hcode(unban)}')
)
