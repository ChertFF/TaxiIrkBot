import asyncio
import logging
import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
import emoji

from filters import IsPrivate
from loader import dp


@dp.message_handler(CommandHelp(), IsPrivate())
async def bot_help(message: types.Message):
    await message.answer(f'{emoji.emojize(":backhand_index_pointing_down:")} {fmt.hbold("Условия для заказа такси: ")} {emoji.emojize(":backhand_index_pointing_down:")}\n'
                         f'1. Вечерняя доставка доступна сотрудникам, чьи смены заканчиваются после 22:00\n'
                         f'2. Записывайся в доставку до 18:00, после этого изменения не принимаются: исключение - стажеры этапа теории и первого месяца работы (резерва)\n'
                         f'3. Утренняя доставка доступна сотрудникам, чьи смены начинаются с 06:30. Записаться на утро и внести изменения можно до 22:00\n'
                         f'4. Ты всегда можешь отказаться от поездки по команде /cancel , но корректным будет считаться отказ не менее, чем за два часа до подачи машины\n'
                         f'5. Выходи к такси вовремя! Подача машин осуществляется на 10 минут каждого часа')
    await asyncio.sleep(1)
    await message.answer(f'{fmt.hbold("Что необходимо сделать для добавления себя в доставку?")}\n'
                         f'В день смены зайти в диалог со мной, ввести команду /order и следовать инструкции. {emoji.emojize(":heart_hands:")}\n')
    await asyncio.sleep(1)
    await message.answer(f'{fmt.hbold("Как можно оставить обратную связь?")}\n'
                         f'Обратную связь по службе такси BiBi или по боту можно оставить с помощью команды /feedback')
    logging.warning( f'Пользователь {message.from_user.id} {message.from_user.full_name} @{message.from_user.username} запросил справку /help | {message.text}')
