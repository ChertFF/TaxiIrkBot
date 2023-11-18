from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

feedback_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Оставить ОС по боту")
        ],
        [
            KeyboardButton(text="Оставить ОС по службе такси")
        ]
,
        [
            KeyboardButton(text="Отменить")
        ]
    ], resize_keyboard=True
)
