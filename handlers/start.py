from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from loguru import logger


@logger.catch()
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /start')
    text = 'Приветствую! 👋 \nЧтобы узнать функционал бота, пропишите комманду /help'
    await message.answer(text)
