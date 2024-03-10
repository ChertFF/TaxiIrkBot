import asyncio
import logging

import aiogram.utils.markdown as fmt
import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove

from data import config
from filters import IsPrivate, InMorningTimeList
from keyboards.default import select_second_time, confim_second_kb, select_city
from keyboards.default.confim_second_order import confim_second_address_kb, confim_second_address_confim_kb
from loader import dp, bot
from states import SecondOrder
from utils.db_api import quick_commands
from utils.misc.check_time import second_check_time
from utils.misc.check_time_second import check_time_second

from utils.notify_admins import send_notify_admins, second_send_notify_admins
from utils.send_media import beats_latecomers

@dp.message_handler(IsPrivate(), text="Утренняя доставка")
async def select_time_morning_order(message: types.Message):
    user = await quick_commands.select_user(message.from_user.id)
    if user.name == None or user.address == None or user.number == None or user.city == None:
        await message.answer(f'Упс! Кажется мы незнакомы. Скорее пройди регистрацию по команде /register\n'
                             f'После этого попробуй записаться в доставку вновь ')
        logging.warning(f'Пользователь {message.from_user.id} выбрал /order, но не прошел регистрацию')
    else:
        await message.answer(
            f"{fmt.hbold('Обрати внимание!')}\n"
            f"{fmt.hbold('Запись в утреннюю доставку доступна сотрудникам, чьи смены начинаются с 06:30.')} \n\n")
        await message.answer(
            f'Подскажи, на какое время тебе нужна доставка? {emoji.emojize(":slightly_smiling_face:")}',
            reply_markup=select_second_time)
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} выбрал /morning_order | Запрос времени')
        await SecondOrder.Time.set()


@dp.message_handler(InMorningTimeList(), state=SecondOrder.Time)
async def set_second_time(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await user.update(second_time=message.text).apply()
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} указал время | Уточнение адреса | {message.text}')
    await message.answer("Давай уточним адрес доставки на работу!")
    if user.second_address == None or user.second_city == None:
        await message.answer(f"Вижу, что у тебя не указан адрес утренней доставки.\n"
                             f"Я могу использовать твой основной адрес: {user.city}, {user.address}?",
                             reply_markup=confim_second_address_kb)
    else:
        await message.answer(f"Тебя нужно забрать по адресу: {user.second_city}, {user.second_address}?",
                             reply_markup=confim_second_address_confim_kb)


@dp.message_handler(IsPrivate(), text="Нет, указать другой адрес", state=SecondOrder.Time)
async def change_second_address(message: types.Message, state: FSMContext):
    await message.answer(f'Осталось уточнить населенный пункт, в который нужна доставка {emoji.emojize(":taxi:")}\n')
    await message.answer(
        f'Обрати внимание, что развоз осуществляется в населенные пункты в удаленности до 25 км от Иркутска.')
    await message.answer(
        f'{emoji.emojize(":backhand_index_pointing_down:")} Выбери населенный пункт с клавиатуры! {emoji.emojize(":backhand_index_pointing_down:")} \n',
        reply_markup=select_city)
    await SecondOrder.City.set()


@dp.message_handler(IsPrivate(), state=SecondOrder.City)
async def change_second_address_confim(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await user.update(second_city=message.text).apply()
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} ввел город на утро| Подтверждение заказа | {message.text}')
    await state.update_data(City_User=message.text)
    await message.answer(f'Осталось уточнить конечный адрес: улицу и номер дома. {emoji.emojize(":taxi:")}\n',
                         reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await message.answer(f'Напиши адрес в формате ниже, чтобы он был легкочетаем для нашего партнера:\n '
                         f'ул. [Название улицы], [№ дома] \n\n'
                         f'Примеры правильно записанных адресов:\n'
                         f'микрорайон Березовый, 44\n'
                         f'проспект Мира, 6\n'
                         f'ул. Ерёменко, 59/3\n')
    await SecondOrder.Address.set()


@dp.message_handler(IsPrivate(), state=SecondOrder.Address)
async def change_second_address_confim(message: types.Message, state: FSMContext):
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} ввел адрес на утро| Подтверждение заказа | {message.text}')
    user = await quick_commands.select_user(message.from_user.id)
    await user.update(second_address=message.text).apply()
    await confim_second_order(message, user)


@dp.message_handler(IsPrivate(), text="Да, можно использовать основной!", state=SecondOrder.Time)
async def confim_second_equial_first(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await user.update(second_address=user.address).apply()
    await user.update(second_city=user.city).apply()
    await message.answer("Готово! Основной адрес теперь совпадает с адресом утренней доставки",
                         reply_markup=ReplyKeyboardRemove())
    await confim_second_order(message, user)
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} указал, что использует основной адрес| Подтверждение заказа | {message.text}')


@dp.message_handler(IsPrivate(), text="Да, адрес указан верно!", state=SecondOrder.Time)
async def second_address_confim(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await confim_second_order(message, user)
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} адрес был указан ранее | Подтверждение заказа | {message.text}')


@dp.message_handler(IsPrivate(), text="Нужно изменить данные на утро", state="*")
async def change_info_message(message: types.Message, state: FSMContext):
    await message.answer("Чтобы изменить данные воспользуйся командой /morning_order",
                         reply_markup=ReplyKeyboardRemove())
    await state.finish()
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} получил отбойник /morning_order| Подтверждение заказа | {message.text}')


#
#
async def confim_second_order(message, user):
    await message.answer(
        f"{emoji.emojize('🌝')} {fmt.hbold('Давай все сверим!')} {emoji.emojize('🌝')} \n\n"
        f"{fmt.hbold('ФИО:')} {user.name}\n"
        f"{fmt.hbold('Населенный пункт: ')} {user.second_city}\n"
        f"{fmt.hbold('Адрес: ')} {user.second_address}\n"
        f"{fmt.hbold('Номер телефона: ')} {user.number}\n"
        f"{fmt.hbold('Время: ')} {user.second_time}\n", reply_markup=confim_second_kb)
    logging.warning(
        f'Пользователь {message.from_user.id} подтверждает заказ | {user.name}, {user.second_city} {user.second_address}, {user.number}, {user.second_time} | Подтверждение заказа')
    await SecondOrder.Confim.set()


@dp.message_handler(IsPrivate(), text="Все корректно!", state=SecondOrder.Confim)
async def change_info(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await state.finish()
    if user.second_time is None:
        await message.answer("Упс! У тебя не указано время доставки", reply_markup=ReplyKeyboardRemove())
    else:
        if second_check_time() is False and user.second_ordered != 1:
            await message.answer(
                f'Увы, добавиться в утреннюю доставку можно было до 18:00 {emoji.emojize(":expressionless_face:")}\n\n',
                reply_markup=ReplyKeyboardRemove())
            logging.warning(
                f'Пользователь {message.from_user.id} поздно добавился в утреннюю доставку | {user.name}, {user.second_city} {user.second_address}, {user.number}, {user.time} | Отказ в записи')
            await second_send_notify_admins(dp, message, user, "Попытка записи в утреннюю доставку после 18:00")
            await beats_latecomers(message)  # Отправляем Леху с молотком
        elif user.second_ordered == 1:
            await message.answer(
                f'Ты уже добавлен в доставку! Все изменения учтены {emoji.emojize(":expressionless_face:")}\n\n',
                reply_markup=ReplyKeyboardRemove())
            await second_send_notify_admins(dp, message, user, "Изменения в доставке на утро")
            logging.warning(
                f'Пользователь {message.from_user.id} изменил данные на утро | {user.name}, {user.second_city} {user.second_address}, {user.number}, {user.time} | Изменения в доставке на утро')
        else:
            await message.answer(f'Готово! Приятного рабочего дня {emoji.emojize(":check_mark:")}',
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer(
                f"Машины будут сформированы к 22:00. После этого времени ты можешь посмотреть сформированную доставку на корпоративной почте.\n")
            await user.update(second_ordered=1).apply()
            await second_send_notify_admins(dp, message, user, "Запись в утреннюю доставку")
            logging.warning(
                f'Пользователь {message.from_user.id} поздно добавился в утреннюю доставку | {user.name}, {user.second_city} {user.second_address}, {user.number}, {user.time} | Отказ в записи')
