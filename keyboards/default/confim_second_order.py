from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


confim_second_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Все корректно!")
        ],
        [
            KeyboardButton(text="Нужно изменить данные на утро")
        ],
        [
            KeyboardButton(text="Отменить")
        ],
    ], resize_keyboard=True
)

confim_second_address_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да, можно использовать основной!")
        ],
        [
            KeyboardButton(text="Нет, указать другой адрес")
        ],
        [
            KeyboardButton(text="Отменить")
        ],
    ], resize_keyboard=True
)

confim_second_address_confim_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да, адрес указан верно!")
        ],
        [
            KeyboardButton(text="Нет, указать другой адрес")
        ],
        [
            KeyboardButton(text="Отменить")
        ],
    ], resize_keyboard=True
)