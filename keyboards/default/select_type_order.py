from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

select_type_order_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Вечерняя доставка")
        ],
        [
            KeyboardButton(text="Утренняя доставка")
        ],
        [
            KeyboardButton(text="Отменить")
        ],
    ], resize_keyboard=True
)
