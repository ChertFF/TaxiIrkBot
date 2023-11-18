from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeCollumn(StatesGroup):
    Collumn = State()
    Value = State()
    chat_id = State()
