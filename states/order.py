from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    Time = State()
    Address = State()
    Confim = State()


class SecondOrder(StatesGroup):
    Time = State()
    Address = State()
    City = State()
    Confim = State()

