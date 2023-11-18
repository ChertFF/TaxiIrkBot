import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from filters import IsPrivate
from loader import dp


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(IsPrivate(), text="Отменить", state="*")
@dp.message_handler(IsPrivate(), text="Отменить отмену", state="*")
@dp.message_handler(Command("reset"), IsPrivate(), state="*")
async def reset_user(message: types.Message, state: FSMContext):
    state_str = await state.get_state()
    await message.answer(f'Готово! Теперь можешь выбрать нужный пункт из меню.', reply_markup=ReplyKeyboardRemove())
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} сбросил state | Неверная комманда, state: {state_str}| {message.text}')
    await state.finish()


@dp.message_handler(IsPrivate(), state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Я тебя не понимаю... Попробуй по-другому!\n"
                         f"Возможно, нужно выбрать вариант с клавиатуры, открой её.\n"
                         f"Она находится справа от поля для ввода текста\n\n\n"
                         f"Если ты случайно выбрал не тот пункт или не ту команду, то воспользуйся командой /reset")
    logging.warning(
        f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} выбрал несуществующую комманду | Неверная комманда, state: {state}| {message.text}')
