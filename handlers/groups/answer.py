import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import IsOurChats
from loader import dp, bot
from states import Answer


@dp.message_handler(Command("answer"), IsOurChats())
async def answer(message: types.Message, state: FSMContext):
    args = message.get_args()
    await Answer.chat_id.set()
    await state.update_data(chat_id=args)
    await message.answer(f'Жду твоего ответа, чтобы переслать его сотруднику! {emoji.emojize("🧐")}')
    await Answer.Answer.set()


@dp.message_handler(IsOurChats(), state=Answer.Answer)
async def answer_state(message: types.Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    data = await state.get_data()
    message_text = data.get("message_text")
    chat_id = data.get("chat_id")
    await bot.send_message(int(chat_id),
                           f'{emoji.emojize("😳")} Внимание! {emoji.emojize("😳")}\n\n'
                           f'Пришел ответ по твоей обратной связи:\n'
                           f'{message_text}\n\n'
                           f'Спасибо за обращение!\n'
                           f'Хорошего дня! {emoji.emojize("🙂")}\n')
    await message.answer(f'Ответ был отправлен! {emoji.emojize("✅")}')
    await state.finish()