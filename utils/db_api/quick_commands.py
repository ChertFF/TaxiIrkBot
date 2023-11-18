from utils.db_api.db_gino import db
from utils.db_api.schemas.user import Users
from asyncpg import UniqueViolationError


async def add_user(chat_id: int, name: str, address=str, number=str, time=str, ordered=int, ban=int):
    try:
        user = Users(chat_id=chat_id, name=name, address=address, number=number, time=time, ordered=ordered, ban=0)
        await user.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')


async def select_all_users():
    users = await Users.query.gino.all()
    return users


async def count_users():
    count = db.func.count(Users.chat_id).gino.scalar()
    return count


async def select_user(chat_id):
    user = await Users.query.where(Users.chat_id == chat_id).gino.first()
    return user


async def select_orders():
    users = await Users.query.where(Users.ordered == 1).gino.all()
    return users


async def select_second_orders():
    users = await Users.query.where(Users.second_ordered == 1).gino.all()
    return users


async def select_reminder():
    users = await Users.query.where(Users.reminder == 1).gino.all()
    return users


async def select_for_everyday_ban():
    users = await Users.query.where(
        (Users.name.is_(None)) &
        (Users.city.is_(None)) &
        (Users.address.is_(None)) &
        (Users.ban == 0) &
        (Users.number.is_(None))
    ).gino.all()
    print(users)
    return users


async def update_user_info(chat_id, new_name, new_address, new_city, new_number):
    user = await select_user(chat_id)
    await user.update(name=new_name).apply()
    await user.update(address=new_address).apply()
    await user.update(city=new_city).apply()
    await user.update(number=new_number).apply()
