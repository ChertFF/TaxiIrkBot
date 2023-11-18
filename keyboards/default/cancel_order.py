from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

select_cancel_order_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отменить вечернюю доставку")
        ],
        [
            KeyboardButton(text="Отменить утреннюю доставку")
        ],
        [
            KeyboardButton(text="Отменить отмену")
        ],
    ], resize_keyboard=True
)