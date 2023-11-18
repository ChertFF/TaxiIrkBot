from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterNew(StatesGroup):
    FI = State()
    Time = State()
    City = State()
    Address = State()
    Number = State()
