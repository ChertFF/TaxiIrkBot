from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsOurChats
from loader import dp, bot
from states import ChangeCollumn
from utils.db_api import quick_commands


@dp.message_handler(Command("change_user_info"), IsOurChats())
async def change_user_info(message: types.Message, state: FSMContext):
    if message.get_args() == "":
        await message.answer(f'Ошибка! Не указан ID пользователя')
    else:
        args = int(message.get_args())
        user = await quick_commands.select_user(args)
        try:
            args = message.get_args()
            await ChangeCollumn.chat_id.set()
            await state.update_data(chat_id_User=args)
            await message.answer(f'Пользователь с ID {user.chat_id} был выбран')
            await message.answer(f'Какие данные по нему ты хочешь изменить?\n'
                                 f'Введи название поля, например: name, address, time, number')
            await ChangeCollumn.Collumn.set()
        except:
            await message.answer(f'Ошибка! Неверно введен ID пользователя')


@dp.message_handler(state=ChangeCollumn.Collumn)
async def set_user_change(message: types.Message, state: FSMContext):
    await state.update_data(Collumn_User=message.text)
    await message.answer("Какое значение ты хочешь задать?")
    await ChangeCollumn.Value.set()


@dp.message_handler(state=ChangeCollumn.Value)
async def set_user_change(message: types.Message, state: FSMContext):
    await state.update_data(Value_User=message.text)
    data = await state.get_data()
    chat_id_User = data.get("chat_id_User")
    Value_User = data.get("Value_User")
    Collumn_User = data.get("Collumn_User")
    user = await quick_commands.select_user(int(chat_id_User))
    if Collumn_User.lower() == 'name':
        await user.update(name=Value_User).apply()
        await message.answer(f'Пользователь с ID {user.chat_id} был изменен')
    elif Collumn_User.lower() == 'address':
        await user.update(address=Value_User).apply()
        await message.answer(f'Пользователь с ID {user.chat_id} был изменен')
    elif Collumn_User.lower() == 'time':
        await user.update(time=Value_User).apply()
        await message.answer(f'Пользователь с ID {user.chat_id} был изменен')
    elif Collumn_User.lower() == 'number':
        await user.update(number=Value_User).apply()
        await message.answer(f'Пользователь с ID {user.chat_id} был изменен')
    elif Collumn_User.lower() == 'ordered':
        Value_User = int(Value_User)
        await user.update(ordered=Value_User).apply()
        await message.answer(f'Пользователь с ID {user.chat_id} был изменен')
    else:
        await message.answer('Такого поля или пользователя не существует, попробуй еще!')
    await state.finish()


