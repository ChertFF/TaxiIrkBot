from aiogram import types
from aiogram.dispatcher.filters import Command
import aiogram.utils.markdown as fmt
from filters import IsOurChats
from loader import dp
from utils.misc.scheduler_task import reset_ordered


@dp.message_handler(Command("admin"), IsOurChats())
async def register(message: types.Message):
    bot_user = await dp.bot.me
    await message.answer(f'{fmt.hbold("Список доступных команд:")}\n'
                         f'/orders_out@{bot_user.username} - получить список записавшихся в доставку\n'
                         f'/morning_orders_out@{bot_user.username} - получить список записавшихся в утреннюю доставку\n'
                         f'/out_all@{bot_user.username} - получить все записи из БД\n'
                         f'Данные выгружаются в формате .xlsx\n\n'
                         f'/logs_out@{bot_user.username} - получить логи с момента последнего запуска бота \n\n'
                         f'/send_all@{bot_user.username} - используется для быстрого и массового оповещения сотрудников при критических ситуациях, например, при ВСМ \n\n'
                         f'/change_user_info@{bot_user.username} [ID] - используется для для ручного изменения данных в БД по конкретному пользователю, использовать в случае ошибок на стороне бота. В остальных случаях рекомендовать менять данные самостоятельно. \n\n'
                         f'{fmt.hbold("Ban&Unban:")}\n'
                         f'/ban@{bot_user.username} [ID] - блокировка пользователя\n'
                         f'/sban@{bot_user.username} [ID] - silence-блокировка пользователя\n'
                         f'/unban@{bot_user.username} [ID] - разблокировка пользователя\n'
                         f'ID пользователя можно получить из /out_all@{bot_user.username}\n'
                         f'Заблокированный пользователь не будет получать ответ на команды или любой тип сообщений.\n'
                         f'Все блокировки просьба согласовывать с мной (@bykov_aa)')


@dp.message_handler(Command("reset_orders"), IsOurChats())
async def reset(message: types.Message):
    await reset_ordered()
