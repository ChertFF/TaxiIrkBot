from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confim_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Все корректно!")
        ],
        [
            KeyboardButton(text="Нужно изменить данные")
        ],
        [
            KeyboardButton(text="Отменить")
        ],
    ], resize_keyboard=True
)
