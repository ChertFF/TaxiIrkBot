from aiogram.dispatcher.filters.state import StatesGroup, State


class SendAllMessage(StatesGroup):
    Send = State()