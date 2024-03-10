import emoji
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from data import config
from filters import IsPrivate
from keyboards.default.feedback import feedback_kb
from loader import bot, dp
from states import FeedBackBot, FeedBackTaxi
from utils.db_api import quick_commands


@dp.message_handler(Command("feedback"), IsPrivate(), state='*')
async def feedback (message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Я нуждаюсь в твоей обратной связи! {emoji.emojize(":smiling_face_with_smiling_eyes:")}\n'
                         f'Подскажи, ты хочешь оставить обратную связь по боту или службе такси?', reply_markup=feedback_kb)


@dp.message_handler(IsPrivate(), text="Оставить ОС по боту")
async def feedback_bot (message: types.Message):
    await message.answer(f'Поделись впечатлениями или подскажи, что во мне можно улучшить! {emoji.emojize(":thinking_face:")}', reply_markup=ReplyKeyboardRemove())
    await FeedBackBot.FeedBack.set()


@dp.message_handler(IsPrivate(), state=FeedBackBot.FeedBack)
async def feedback_bot_state(message: types.Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    data = await state.get_data()
    message_text = data.get("message_text")
    await bot.send_message(config.ADMIN_CHAT_ID, f'{emoji.emojize(":exploding_head:")} Внимание вопрос! {emoji.emojize(":exploding_head:")}\n\n'
                                           f'Поступила обратная связь от сотрудника по боту:\n'
                                           f'{message_text}\n'
                                           f'Отправил: {message.from_user.full_name} | @{message.from_user.username}\n\n'
                                           f'Я пообещал, что сотруднику ответят, будет нехорошо нарушить данное обещание.\n'
                                           f'Чтобы ответить ему напиши: /answer {message.chat.id}')
    await message.answer(f"Обратная связь принята, твой ответ передан разработчику.\n"
                         f"В ближайшее время мы тебе ответим! {emoji.emojize(':check_mark:')}")

    await state.finish()


@dp.message_handler(IsPrivate(), text="Оставить ОС по службе такси")
async def feedback_taxi (message: types.Message):
    await message.answer(f'Поделись обратной связью о нашем партнере 222-222! {emoji.emojize(":thinking_face:")}\n'
                         f'Если ты хочешь оставить жалобу или пожелание, то в подробностях опиши ситуацию, не забыв указать дату и время случившегося.\n'
                         f'Мы ответим тебе в самое ближайшее время! {emoji.emojize(":winking_face:")}', reply_markup=ReplyKeyboardRemove())
    await FeedBackTaxi.FeedBack.set()


@dp.message_handler(IsPrivate(), state=FeedBackTaxi.FeedBack)
async def feedback_bot_state(message: types.Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    data = await state.get_data()
    message_text = data.get("message_text")
    await bot.send_message(config.ADMIN_CHAT_ID, f'{emoji.emojize(":exploding_head:")} Внимание вопрос! {emoji.emojize(":exploding_head:")}\n\n'
                                           f'Поступила обратная связь от сотрудника по 222-222:\n'
                                           f'{message_text}\n'
                                           f'Отправил: {message.from_user.full_name} | @{message.from_user.username}\n\n'
                                           f'Я пообещал, что сотруднику ответят, будет нехорошо нарушить данное обещание.\n'
                                           f'Чтобы ответить ему напиши: /answer {message.chat.id}')
    await message.answer(f"Обратная связь по такси 222-222 принята! \n"
                         f"В ближайшее время мы тебе ответим! {emoji.emojize(':check_mark:')}")
    await state.finish()