from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список комманд',
        '/start - запустить бота',
        '/help - получить справку',
        '/find_book - поиск книги по названию'
    ]

    await message.answer('\n'.join(text))
