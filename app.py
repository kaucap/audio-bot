from bot_commands import set_default_commands


async def on_startup(dp):
    await set_default_commands(dp)
    print('Запуск бота')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
