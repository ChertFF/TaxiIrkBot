import asyncio
import logging

import aiogram.utils.markdown as fmt
import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.base import Integer

from data.config import CITY_LIST
from filters import IsPrivate, InCityList
from keyboards.default import select_city
from loader import dp
from states import RegisterNew
from utils.db_api import quick_commands
from utils.regular_expressions import correct_phone_number, correct_FI


@dp.message_handler(Command("register"), IsPrivate())
async def register(message: types.Message):
    await message.answer(f'Подскажи, пожалуйста, Фамилию, Имя и Отчество! {emoji.emojize(":eyes:")}\n')
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} начал регистрацию | Запрос ФИО | {message.text}')
    await RegisterNew.FI.set()


@dp.message_handler(state=RegisterNew.FI)
async def set_FI(message: types.Message, state: FSMContext):
    while correct_FI(message.text) == "error":
        await message.answer(
            f'Увы, мне что-то подсказывает, что людей с таким ФИО нет. {emoji.emojize(":expressionless_face:")}\n'
            f'Давай попробуем еще раз!\n')
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} неверно ввел ФИО | Запрос ФИО | {message.text}')
        return
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} ввел ФИО | Запрос номера | {message.text}')
    await state.update_data(FI_User=message.text)
    await message.answer(f'Приятно познакомиться! Какой у тебя номер телефона?! {emoji.emojize(":mobile_phone:")}\n'
                         f'Мне он необходим, чтобы служба такси могла с тобой связаться.\n'
                         f'Укажи его в формате +79#########.')
    await RegisterNew.Number.set()


@dp.message_handler(state=RegisterNew.Number)
async def set_Number(message: types.Message, state: FSMContext):
    while correct_phone_number(message.text) == "error":
        await message.answer(
            f'Увы, ты указал номер в неверном формате, бот не может его воспринять. {emoji.emojize(":expressionless_face:")}\n'
            f'Введи корректный номер телефона в формате +79#########\n')
        logging.warning(
            f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} неверно ввел номер | Запрос номера | {message.text}')
        return
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} ввел номер | Запрос города | {message.text}')
    await state.update_data(Number_User=message.text)
    await message.answer(f'Осталось уточнить населенный пункт, в который нужна доставка {emoji.emojize(":taxi:")}\n')
    await asyncio.sleep(1)
    await message.answer(
        f'Обрати внимание, что развоз осуществляется в населенные пункты в удаленности до 25 км от Иркутска.')
    await message.answer(
        f'{emoji.emojize(":backhand_index_pointing_down:")} Выбери населенный пункт с клавиатуры! {emoji.emojize(":backhand_index_pointing_down:")} \n',
            reply_markup=select_city)
    await RegisterNew.City.set()


@dp.message_handler(InCityList(), state=RegisterNew.City)
async def set_City(message: types.Message, state: FSMContext):
    # print(message.text)
    # print(select_city.)
    # while message.text != "г. Ростов" or message.text != "г. Батайск" or message.text != "г. Аскай" or message.text != "хутор Ленинакан":
    #     await message.answer( f'Увы, ты выбрал населенный пункт не с клавиатуры, бот не может его воспринять. {emoji.emojize(":expressionless_face:")}\n'
    #                           f'Клавиатура находится рядом с полем для ввода текста, используй её!')
    #     logging.warning(
    #         f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} неверно ввел город | Запрос города | {message.text}')
    #     return
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} ввел город | Запрос адреса | {message.text}')
    await state.update_data(City_User=message.text)
    await message.answer(f'Осталось уточнить конечный адрес: улицу и номер дома. {emoji.emojize(":taxi:")}\n', reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(1)
    await message.answer(f'Напиши адрес в формате ниже, чтобы он был легкочетаем для нашего партнера:\n '
                         f'ул. [Название улицы], [№ дома] \n\n'
                         f'Примеры правильно записанных адресов:\n'
                         f'микрорайон Березовый, 44\n'
                         f'проспект Мира, 6\n'
                         f'ул. Ерёменко, 59/3\n')
    await RegisterNew.Address.set()



@dp.message_handler(state=RegisterNew.Address)
async def set_Address(message: types.Message, state: FSMContext):
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} ввел адрес | Завершение регистрации | {message.text}')
    await state.update_data(Address_User=message.text)
    data = await state.get_data()
    chat_id: Integer = message.from_user.id
    FI_User = data.get("FI_User")
    Number_User = data.get("Number_User")
    Address_User = data.get("Address_User")
    City_User = data.get("City_User")

    await message.answer(
        f"{fmt.hbold('Давай все сверим!')}\n"
        f"Если данные некорректны, то можешь заново их указать по команде /changeinfo\n\n"
        f"{fmt.hbold('ФИО: ')} {FI_User}\n"
        f"{fmt.hbold('Номер телефона: ')} {Number_User}\n"
        f"{fmt.hbold('Населенный пункт: ')} {City_User}\n"
        f"{fmt.hbold('Адрес: ')} {Address_User}\n")
    await asyncio.sleep(1)
    await message.answer(
        f"{fmt.hbold('Теперь о том, как добавить себя в доставку... ')}\n"
        f"В день смены до 18:00 тебе необходимо ввести команду /order или выбрать ее из меню. После этого мы сверим корректность данных и добавим тебя в доставку.\n\n"
        f"{fmt.hbold('Ознакомиться с правилами по заказу такси можно по команде /help')}")

    await quick_commands.update_user_info(message.from_user.id, FI_User, Address_User, City_User, Number_User)
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} завершил регистрацию | {message.from_user.id}, {FI_User}, {Address_User}, {Number_User}, {Address_User}|')
    await state.finish()
