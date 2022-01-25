from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from loguru import logger


@logger.catch()
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /help')
    text = [
        'Список комманд',
        '/start - запустить бота 💻',
        '/help - получить справку 📣',
        '/find_book - поиск книги по названию 🔍',
        '/new_book - поиск новых книг 🆕',
        '/best_book - поиск лучших книг ⭐️',
        '/paid_book - поиск платных книг 💰',
        '/genres - поиск книг по жанрам ✅'
    ]

    await message.answer('\n'.join(text))
