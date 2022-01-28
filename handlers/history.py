from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from db_api import sql_commands as command
from db_api.schemas.user import User
from loader import dp


@logger.catch()
@dp.message_handler(Command("history"))
async def show_hotel_history(message: types.Message):
    user = await User.get(message.from_user.id)
    search_information = await command.choose_info(user.id)
    logger.info(f'Клиент с id: {message.from_user.id} запросил историю поиска книг')
    if len(search_information) > 0:
        for info in search_information:
            await message.answer(info.request)
    else:
        await message.answer('История поиска книг пуста')
