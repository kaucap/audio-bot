from bot_commands import set_default_commands
from loguru import logger


logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 week",
           compression="zip")


@logger.catch()
async def on_startup(dp):
    await set_default_commands(dp)
    logger.info('Запуск бота')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
