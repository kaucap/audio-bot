from bot_commands import set_default_commands
from loguru import logger
from db_api import db_gino
from db_api.db_gino import db
from middlewares.throttling import ThrottlingMiddleware

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 week",
           compression="zip")


@logger.catch()
async def on_startup(dp):

    await set_default_commands(dp)
    logger.info('Запуск бота')

    logger.info('Подключаем БД')
    await db_gino.on_startup(dp)

    logger.info('Создаем таблицы')
    await db.gino.create_all()

    logger.info('Бот готов к работе')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    dp.middleware.setup(ThrottlingMiddleware())
    executor.start_polling(dp, on_startup=on_startup)