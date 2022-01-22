from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_time = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='День'),
            KeyboardButton(text='Неделя')
        ],
        [
            KeyboardButton(text='Месяц'),
            KeyboardButton(text='За всё время')
        ]
    ],
    resize_keyboard=True
)
