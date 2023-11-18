import asyncio

from data import config
from utils.db_api import quick_commands
from utils.db_api.db_gino import db


async def db_test():
    await db.set_bind(config.POSTGRES_URL)
    await db.gino.drop_all()
    await db.gino.create_all()
    print('11111')
    await quick_commands.add_user(12312312312, 'Vlad', 'asdasd', '+79025606162', None, None)
    users = await quick_commands.select_all_users()
    print(users)


loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
