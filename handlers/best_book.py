from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from keyboard.default.period_of_time_buttons import choose_time
from loader import dp, bot
from states import BestBook
from utils.handlers.best_book import send_results_duration_month, send_results_duration_week, \
    send_results_duration_all_time, selected_time_day
from utils.handlers.common import clear_user_history_if_reach_limit, user_wants_see_next_page


@logger.catch()
@dp.message_handler(Command("best_book"))
@dp.throttled(rate=5)
async def looking_new_book(message: types.Message):
    request = 'Поиск лучших книг'
    await clear_user_history_if_reach_limit(message=message, request=request)
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /best_book')
    await message.answer('Выберите за какой промежуток времени мне вывести лучшие книги?', reply_markup=choose_time)
    await BestBook.choice.set()


@logger.catch()
@dp.message_handler(state=BestBook.choice)
async def choosing_time(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'День ✨':
        await selected_time_day(state=state, message=message, bot=bot)
    elif answer == 'Неделя 💫':
        await send_results_duration_week(bot=bot, state=state, message=message)
    elif answer == 'Месяц ⭐️':
        await send_results_duration_month(bot=bot, state=state, message=message)
    elif answer == 'За всё время 💥':
        await send_results_duration_all_time(bot=bot, state=state, message=message)
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов!')
        await BestBook.choice.set()


@logger.catch()
@dp.message_handler(state=BestBook.next_page)
async def next_page(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        current_command = 'best_book'
        information_for_search_books = {'command': current_command, 'message': message, 'state': state,
                                        'bot': bot, 'current_state': BestBook}
        await user_wants_see_next_page(information_for_search_books)
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Хорошо, поиск книг завершен.\nЧтобы узнать весь функционал введите комманду /help',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await BestBook.next_page.set()
