import asyncio
import logging

from aiogram import executor
from datetime import datetime, timedelta
import datetime
from data import config
from loader import dp
import middlewares, filters, handlers
from utils import on_startup_notify
from utils.misc.scheduler_task import scheduler_reset_ordered
from utils.set_bot_commands import set_default_commands
from loader import db
from utils.db_api.db_gino import on_startup as on_start_gino
import aioschedule



async def on_startup(dispatcher):
    await on_start_gino(dp)
    # print('Удаление таблиц')
    # await db.gino.drop_all()
    # print('Создание таблиц')
    # await db.gino.create_all()

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    await on_startup_notify(dp)

    asyncio.create_task(scheduler_reset_ordered())
    # asyncio.create_task(scheduler_send_reminder())
    logging.warning('Bot started!')
    print(datetime.datetime.now().time())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
