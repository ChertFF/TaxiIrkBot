import asyncio
import logging

import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text

from data import config
from data.config import CITY_LIST
from filters import IsPrivate, InCityList
from handlers.users.order import select_time_order, confim_order, info_order
from keyboards.default import change_info_kb, select_city
from loader import dp, bot
from utils import correct_phone_number
from utils.db_api import quick_commands
from states import ChangeAddress, ChangeNumber, ChangeFI, Order
from utils.misc.check_time import check_time
from utils.notify_admins import send_notify_admins
from utils.regular_expressions import correct_FI
from utils.send_media import beats_latecomers


@dp.message_handler(Command("changeinfo"), IsPrivate(), state='*')
@dp.message_handler(IsPrivate(), text="Нужно изменить данные", state=Order.Confim)
async def change_info(message: types.Message, state: FSMContext):
    await state.finish()
    user = await quick_commands.select_user(message.from_user.id)
    if check_time() is False:
        await message.answer(
            f'Увы, изменить данные по доставке возможно до 18:00 {emoji.emojize(":expressionless_face:")}',
            reply_markup=ReplyKeyboardRemove())
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} изменить данные по заказу после 18:00 | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Отказ в изменении')
        await beats_latecomers(message)  # Отправляем Леху с молотком

    else:
        await message.answer(f"Давай изменим данные, что именно ты хочешь поменять?\n"
                             f"Выбери пункт из появившегося меню!", reply_markup=change_info_kb)
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} выбрал /changeingo | Изменение данных | {message.text}')
    await state.finish()


@dp.message_handler(IsPrivate(), text="Нужно изменить время")
async def change_time(message: types.Message, state: FSMContext):
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} выбрал изменить время | Изменение времени | {message.text}')
    await select_time_order(message, state)


@dp.message_handler(IsPrivate(), text="Нужно изменить адрес")
async def change_city(message: types.Message):
    await message.answer(f'Осталось уточнить населенный пункт, в который нужна доставка {emoji.emojize(":taxi:")}\n')
    await message.answer(
        f'Обрати внимание, что развоз осуществляется в населенные пункты в удаленности до 25 км от Иркутска.')
    await message.answer(
        f'{emoji.emojize(":backhand_index_pointing_down:")} Выбери населенный пункт с клавиатуры! {emoji.emojize(":backhand_index_pointing_down:")} \n',
        reply_markup=select_city)
    await ChangeAddress.City.set()


@dp.message_handler(InCityList(), state=ChangeAddress.City)
async def change_city_state(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await user.update(city=message.text).apply()
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} ввел город | Запрос адреса | {message.text}')
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
    await ChangeAddress.Address.set()


@dp.message_handler(state=ChangeAddress.Address)
async def change_address_state(message: types.Message, state: FSMContext):
    user = await quick_commands.select_user(message.from_user.id)
    await state.finish()
    if check_time() is False and user.ordered == 1:
        await message.answer(
            f'Увы, изменить данные по доставке возможно до 18:00 {emoji.emojize(":expressionless_face:")}',
            reply_markup=ReplyKeyboardRemove())
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} пытался изменить данные по заказу после 18:00 | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Отказ в изменении')
    elif check_time() is True and user.ordered == 1:
        await message.answer(f'Готово! Данные о тебе изменены {emoji.emojize(":check_mark:")}',
                             reply_markup=ReplyKeyboardRemove())
        await user.update(address=message.text).apply()
        await info_order(message, user)
        await send_notify_admins(dp, message, user, "Изменения в доставке")
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} измененил данные по заказу | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Изменения в заказе')

    else:
        await user.update(address=message.text).apply()
        logging.warning(f'Пользователь {message.from_user.id} указал время | Подтверждение заказа | {message.text}')
        await confim_order(message, user)

        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} измененил данные по заказу | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Изменения в заказе')


@dp.message_handler(IsPrivate(), text="Нужно изменить номер телефона")
async def change_number(message: types.Message):
    await message.answer(f'Какой у тебя номер телефона?!\n'
                         f'Укажи его в формате +79#########.', reply_markup=ReplyKeyboardRemove())
    await ChangeNumber.Number.set()
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} выбрал изменить номер | Изменение номера | {message.text}')


@dp.message_handler(IsPrivate(), state=ChangeNumber.Number)
async def change_number_state(message: types.Message, state: FSMContext):
    await state.finish()
    user = await quick_commands.select_user(message.from_user.id)
    while correct_phone_number(message.text) == "error":
        await message.answer(
            f'Увы, ты указал номер в неверном формате, бот не может его воспринять. {emoji.emojize(":expressionless_face:")}\n'
            f'Введи корректный номер телефона в формате +79#########\n')
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} неверно ввел номер | Запрос номера | {message.text}')
        return
    if check_time() is False and user.ordered == 1:
        await message.answer(
            f'Увы, изменить данные по доставке возможно до 18:00 {emoji.emojize(":expressionless_face:")}',
            reply_markup=ReplyKeyboardRemove())
        logging.warning(
            f'Пользователь {message.from_user.id} пытался изменить данные по заказу после 18:00 | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Отказ в изменении')
        await state.finish()
    elif check_time() is True and user.ordered == 1:
        await message.answer(f'Готово! Данные о тебе изменены {emoji.emojize(":check_mark:")}',
                             reply_markup=ReplyKeyboardRemove())
        await user.update(number=message.text).apply()
        await info_order(message, user)
        await send_notify_admins(dp, message, user, "Изменения в доставке")
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} измененил данные по заказу | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Изменения в заказе')
    else:
        await user.update(number=message.text).apply()
        logging.warning(f'Пользователь {message.from_user.id} указал время | Подтверждение заказа | {message.text}')
        await confim_order(message, user)

        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} измененил данные по заказу | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Изменения в заказе')


@dp.message_handler(IsPrivate(), text="Нужно изменить ФИО")
async def change_FI(message: types.Message):
    await message.answer(f'Подскажи, пожалуйста, Фамилию, Имя и Отчество.\n', reply_markup=ReplyKeyboardRemove())
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} выбрал изменить ФИО | Изменение ФИО | {message.text}')
    await ChangeFI.FI.set()


@dp.message_handler(IsPrivate(), state=ChangeFI.FI)
async def change_FI_state(message: types.Message, state: FSMContext):
    await state.update_data(FI_User=message.text)
    user = await quick_commands.select_user(message.from_user.id)
    await state.finish()
    while correct_FI(message.text) == "error":
        await message.answer(
            f'Увы, мне что-то подсказывает, что людей с таким ФИО нет. {emoji.emojize(":expressionless_face:")}\n'
            f'Давай попробуем еще раз!\n')
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} неверно ввел ФИО | Запрос ФИО | {message.text}')
        return
    if check_time() is False and user.ordered == 1:
        await message.answer(
            f'Увы, изменить данные по доставке возможно до 18:00 {emoji.emojize(":expressionless_face:")}',
            reply_markup=ReplyKeyboardRemove())
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} пытался изменить данные по заказу после 18:00 | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Отказ в изменении')
        await state.finish()
    elif check_time() is True and user.ordered == 1:
        await message.answer(f'Готово! Данные о тебе изменены {emoji.emojize(":check_mark:")}',
                             reply_markup=ReplyKeyboardRemove())
        await user.update(name=message.text).apply()
        await info_order(message, user)
        await send_notify_admins(dp, message, user, "Изменения в доставке")
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} измененил данные по заказу | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Изменения в заказе')

    else:
        await user.update(name=message.text).apply()
        logging.warning(f'Пользователь {message.from_user.id} указал время | Подтверждение заказа | {message.text}')
        await confim_order(message, user)

        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} измененил данные по заказу | {user.name},{user.city} {user.address}, {user.number}, {user.time} | Изменения в заказе')
