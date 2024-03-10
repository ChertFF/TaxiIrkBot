from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("order", "Записаться в доставку"),
            types.BotCommand("cancel", "Отказаться от доставки"),
            types.BotCommand("changeinfo", "Изменить данные по доставке"),
            types.BotCommand("info", "Посмотреть данные о себе"),
            types.BotCommand("remind_me", "Управление напоминаниями"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("feedback", "Оставить ОС по боту или 222-222"),
        ]
    )
