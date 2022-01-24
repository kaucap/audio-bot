from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_type = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Новые 🆕'),
            KeyboardButton(text='Лучшие 🔥')
        ],
        [
            KeyboardButton(text='Обсуждаемые 🗣'),
        ]
    ],
    resize_keyboard=True
)
