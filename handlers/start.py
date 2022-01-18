from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = 'Приветствую! 👋 \nЧтобы узнать функционал бота, пропишите комманду /help'
    await message.answer(text)
