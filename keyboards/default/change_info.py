from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

change_info_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Нужно изменить время")
        ],
        [
            KeyboardButton(text="Нужно изменить адрес")
        ],
        [
            KeyboardButton(text="Нужно изменить номер телефона")
        ],
        [
            KeyboardButton(text="Нужно изменить ФИО")
        ],
        [
            KeyboardButton(text="Отменить")
        ],
    ], resize_keyboard=True
)