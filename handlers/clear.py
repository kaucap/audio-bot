from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from db_api.schemas.user_request import Info
from db_api.schemas.user import User
from loader import dp


@logger.catch()
@dp.message_handler(Command("clear"))
async def clear_hotel_history(message: types.Message):
    logger.info(f'Клиент с id: {message.from_user.id} очистил историю поиска')
    user = await User.get(message.from_user.id)
    await Info.delete.where(user.id == Info.id).gino.status()
    await message.answer('История поиска книг удалена 🚮')
