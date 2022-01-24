from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

genres = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Фантастика 🛸'),
            KeyboardButton(text='Детективы 🕵️‍♂️'),
        ],
        [
            KeyboardButton(text='Роман ❤️'),
            KeyboardButton(text='Психология 📚'),
        ],
        [
            KeyboardButton(text='Классика ✨'),
            KeyboardButton(text='Ужасы 👀'),
        ]
    ],
    resize_keyboard=True
)
