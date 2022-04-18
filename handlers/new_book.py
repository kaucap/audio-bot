from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from keyboard.default.next_page_buttons import choice
from loader import dp, bot
from request import find_new_book
from states import FindNewBook
from utils.book_information import if_search_results_have_pages
from utils.handlers.common import clear_user_history_if_reach_limit, send_results_to_user, user_wants_see_next_page


@logger.catch()
@dp.message_handler(Command("new_book"))
async def looking_new_book(message: types.Message):
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /new_book')
    await message.answer('Приступаем к поиску новых книг? :)', reply_markup=choice)
    await FindNewBook.book.set()


@logger.catch()
@dp.message_handler(state=FindNewBook.book)
async def result(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        request = 'Поиск новых книг'
        await clear_user_history_if_reach_limit(message=message, request=request)
        logger.info('Бот приступил к выполнению команды /new_book')
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        book_result = await find_new_book(message=message, bot=bot)
        pages = await if_search_results_have_pages(book_result)
        information_for_search_books = {'pages': pages, 'state': state, 'message': message,
                                        'current_state': FindNewBook}
        await send_results_to_user(information_for_search_books)
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Вы отменили поиск книг. Для ознакомления со всем функционалом '
                             'бота введите /help', reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await FindNewBook.book.set()


@logger.catch()
@dp.message_handler(state=FindNewBook.next_page)
async def result(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        current_command = 'new_book'
        information_for_search_books = {'command': current_command, 'message': message, 'state': state,
                                        'bot': bot, 'current_state': FindNewBook}
        await user_wants_see_next_page(information_for_search_books)
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Хорошо, поиск книг завершен.\nЧтобы узнать весь функционал введите комманду /help',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await FindNewBook.next_page.set()
