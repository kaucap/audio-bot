from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота 💻"),
        types.BotCommand("help", "Помощь 📣"),
        types.BotCommand("find_book", "Поиск книги по автору или названию 🔍"),
        types.BotCommand("new_book", "Поиск новых книг 🆕"),
        types.BotCommand("best_book", "Поиск лучших книг ⭐️"),
        types.BotCommand("paid_book", "Поиск платных книг 💰"),
        types.BotCommand("genres", "Поиск книг по жанрам ✅")
    ])
