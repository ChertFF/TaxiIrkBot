from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeAddress(StatesGroup):
    Address = State()
    City = State()


class ChangeFI(StatesGroup):
    FI = State()


class ChangeNumber(StatesGroup):
    Number = State()
