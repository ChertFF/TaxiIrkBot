from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedBackBot(StatesGroup):
    FeedBack = State()


class FeedBackTaxi(StatesGroup):
    FeedBack = State()


class Answer(StatesGroup):
    Answer = State()
    chat_id = State()
