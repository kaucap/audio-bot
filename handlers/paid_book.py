from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from keyboard.default.type_of_book_buttons import choose_type
from loader import dp, bot
from states import PaidBook
from utils.handlers.common import clear_user_history_if_reach_limit, user_wants_see_next_page
from utils.handlers.paid_book import send_paid_book_results_new, send_paid_book_results_best, \
    send_paid_book_results_popular


@logger.catch()
@dp.message_handler(Command("paid_book"))
async def looking_new_book(message: types.Message):
    request = 'Поиск платных книг'
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /paid_book')
    await message.answer('Выберите вид книг', reply_markup=choose_type)
    await clear_user_history_if_reach_limit(message=message, request=request)
    await PaidBook.book.set()


@logger.catch()
@dp.message_handler(state=PaidBook.book)
async def choosing_type_of_book(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Новые 🆕':
        await send_paid_book_results_new(message=message, bot=bot, state=state)
    elif answer == 'Лучшие 🔥':
        await send_paid_book_results_best(message=message, bot=bot, state=state)
    elif answer == 'Обсуждаемые 🗣':
        await send_paid_book_results_popular(message=message, bot=bot, state=state)
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов!"')
        await PaidBook.book.set()


@logger.catch()
@dp.message_handler(state=PaidBook.next_page)
async def next_page_book(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        current_command = 'paid_book'
        information_for_search_books = {'command': current_command, 'message': message, 'state': state,
                                        'bot': bot, 'current_state': PaidBook}
        await user_wants_see_next_page(information_for_search_books)
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Хорошо, поиск книг завершен.\nЧтобы узнать весь функционал введите комманду /help',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await PaidBook.next_page.set()
