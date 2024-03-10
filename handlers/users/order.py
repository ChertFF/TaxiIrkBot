import asyncio
import logging

import emoji
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from data import config
from filters import IsPrivate, InTimeList
from keyboards.default import select_time, confim_kb, select_type_order_kb
from loader import dp, bot
from aiogram import types

from states import Order
from utils.db_api import quick_commands
from utils.misc import check_time

import aiogram.utils.markdown as fmt

from utils.notify_admins import send_notify_admins
from utils.send_media import third_sept, beats_latecomers, wow


@dp.message_handler(Command("order"), IsPrivate(), state='*')
async def select_time_order(message: types.Message, state: FSMContext):
    await state.finish()
    # await message.answer(
    #     f"{fmt.hbold('ВАЖНО!')}\n", reply_markup=ReplyKeyboardRemove())
    # await asyncio.sleep(1)
    # await message.answer(
    #     f"{fmt.hbold('C 11.03 интервал записи в утренний развоз будет ограничен:')}\n"
    #     f"было - до 22:00, стало - до 18:00. \n\n"
    #     f"Изменения проводятся с целью, чтобы вы могли получать распределение по утренним машинам намного раньше!")
    # await wow(message)  # Отправляем Леху довольного
    # await asyncio.sleep(3)
    await message.answer(f'Подскажи, какой тип доставки тебя интересует?', reply_markup=select_type_order_kb)


@dp.message_handler(IsPrivate(), text="Вечерняя доставка")
async def select_time_order(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    if user.name == None or user.address == None or user.number == None or user.city == None:
        await message.answer(f'Упс! Кажется мы незнакомы. Скорее пройди регистрацию по команде /register\n'
                             f'После этого попробуй записаться в доставку вновь {emoji.emojize(":smiling_face_with_sunglasses:")}', reply_markup=ReplyKeyboardRemove())
        logging.warning(f'Пользователь {message.from_user.id} выбрал /order, но не прошел регистрацию')
        await state.finish()
    else:
        await message.answer(
            f"{fmt.hbold('Обрати внимание!')}\n"
            f"{fmt.hbold('Запись в доставку и изменение данных по заказу доступно до 18:00')} \n\n")
        await message.answer(
            f'Подскажи, на какое время тебе нужна доставка? {emoji.emojize(":slightly_smiling_face:")}',
            reply_markup=select_time)
        logging.warning(f'Пользователь {message.from_user.id} выбрал /order | Запрос времени')
        await Order.Time.set()


@dp.message_handler(InTimeList(), state=Order.Time)
async def set_time(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await state.finish()
    if check_time() is False and user.ordered == 1:
        await message.answer(
            f'Увы, изменить данные по доставке возможно до 18:00 {emoji.emojize(":expressionless_face:")}',
            reply_markup=ReplyKeyboardRemove())
        logging.warning(
            f'Пользователь {message.from_user.id} пытался изменить данные после 18:00 | {user.name}, {user.address}, {user.number}, {message.text} | Отказ в изменении')
        await send_notify_admins(dp, message, user, "Попытка изменений после 18:00")
        await beats_latecomers(message) #Отправляем Леху с молотком
    elif check_time() is True and user.ordered == 1:
        await message.answer(f'Готово! Данные о тебе изменены {emoji.emojize(":check_mark:")}',
                             reply_markup=ReplyKeyboardRemove())
        await user.update(time=message.text).apply()
        await info_order(message, user)
        await send_notify_admins(dp, message, user, "Изменения в доставке")
        logging.warning(
            f'Пользователь {message.from_user.id} измененил данные по заказу | {user.name}, {user.city} {user.address}, {user.number}, {user.time} | Изменения в заказе')
    else:
        await user.update(time=message.text).apply()
        logging.warning(f'Пользователь {message.from_user.id} указал время | Подтверждение заказа | {message.text}')
        await confim_order(message, user)


async def confim_order(message, user):
    await message.answer(
        f"{emoji.emojize(':backhand_index_pointing_down:')} {fmt.hbold('Давай все сверим!')} {emoji.emojize(':backhand_index_pointing_down:')} \n\n"
        f"{fmt.hbold('ФИО:')} {user.name}\n"
        f"{fmt.hbold('Населенный пункт: ')} {user.city}\n"
        f"{fmt.hbold('Адрес: ')} {user.address}\n"
        f"{fmt.hbold('Номер телефона: ')} {user.number}\n"
        f"{fmt.hbold('Время: ')} {user.time}\n", reply_markup=confim_kb)
    logging.warning(f'Пользователь {message.from_user.id} подтверждает заказ | {message.text};{user.name};{user.city} {user.address}; {user.number} | Подтверждение заказа')
    await Order.Confim.set()


async def info_order(message, user):
    await message.answer(
        f"{emoji.emojize(':backhand_index_pointing_down:')} {fmt.hbold('Данные по твоему заказу')} {emoji.emojize(':backhand_index_pointing_down:')} \n\n"
        f"{fmt.hbold('ФИО:')} {user.name}\n"
        f"{fmt.hbold('Населенный пункт:')} {user.city}\n"
        f"{fmt.hbold('Адрес:')} {user.address}\n"
        f"{fmt.hbold('Номер телефона: ')} {user.number}\n"
        f"{fmt.hbold('Время: ')} {user.time}\n", reply_markup=ReplyKeyboardRemove())
    if user.ordered == 1:
        await message.answer(f"{fmt.hbold('Ты добавлен в доставку!')}\n", reply_markup = ReplyKeyboardRemove())
    else:
        await message.answer(f"{fmt.hbold('Ты не добавлен в доставку!')}\n", reply_markup = ReplyKeyboardRemove())
    logging.warning(
        f'Пользователь {message.from_user.id} посмотрел данные по заказу | {message.text};{user.name};{user.city} {user.address}; {user.number} | Инфо по заказу')


@dp.message_handler(IsPrivate(), text="Все корректно!", state=Order.Confim)
async def change_info(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await state.finish()
    if user.time is None:
        await message.answer("Упс! У тебя не указано время доставки",reply_markup = ReplyKeyboardRemove())
    else:
        if check_time() is False and user.ordered != 1:
            await message.answer(
                f'Увы, добавиться в доставку можно было до 18:00 {emoji.emojize(":expressionless_face:")}\n\n'
                f"Исключение: стажеры первого месяца работы и этапа теории могут добавиться в доставку после 18:00, обратившись к дежурному супервизору, наставнику или руководителю\n",
                reply_markup=ReplyKeyboardRemove())
            logging.warning(
                f'Пользователь {message.from_user.id} поздно добавился в доставку | {user.name}, {user.city} {user.address}, {user.number}, {user.time} | Отказ в записи')
            await send_notify_admins(dp, message, user, "Попытка записи в доставку после 18:00")
            await beats_latecomers(message)  # Отправляем Леху с молотком
        elif user.ordered == 1:
            await message.answer(f'Ты уже добавлен в доставку! Все изменения учтены {emoji.emojize(":expressionless_face:")}\n\n')
        else:
            await message.answer(f'Готово! Приятного рабочего дня {emoji.emojize(":check_mark:")}',
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer(
                f"Машины будут сформированы к 20:00. После этого времени ты можешь посмотреть сформированную доставку на корпоративной почте.\n")
            await user.update(ordered=1).apply()
            await send_notify_admins(dp, message, user, "Запись в доставку")
            logging.warning(
                f'Пользователь {message.from_user.id} записался в доставку | {user.name}, {user.city} {user.address}, {user.number}, {user.time} | Заказ добавлен')

