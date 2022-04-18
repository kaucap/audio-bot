import aiogram
import bs4
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from keyboard.default.next_page_buttons import choice
from request import best_book_day, best_book_week, best_book_month, best_book_all_time
from states import BestBook
from utils.book_information import if_search_results_have_pages
from utils.handlers.common import there_are_no_books, send_results_to_user


async def selected_time_day(message: types.Message, bot: aiogram.Bot, state: FSMContext):
    logger.info('Бот приступил к выполнению команды /best_book')
    await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
    await best_book_day(message=message, bot=bot)
    await message.answer('Книг больше нет')
    await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
    await state.reset_state()


async def book_results_duration_week(message: types.Message, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /best_book')
    await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
    book_result = await best_book_week(message=message, bot=bot)
    return book_result


async def send_results_duration_week(message, bot, state):
    book_result = await book_results_duration_week(message=message, bot=bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': BestBook}
    await send_results_to_user(information_for_search_books)


async def book_results_duration_month(message: types.Message, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /best_book')
    await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
    book_result = await best_book_month(message=message, bot=bot)
    return book_result


async def send_results_duration_month(message, bot, state):
    book_result = await book_results_duration_month(message=message, bot=bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': BestBook}
    await send_results_to_user(information_for_search_books)


async def book_results_duration_all_time(message: types.Message, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /best_book')
    await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
    book_result = await best_book_all_time(message=message, bot=bot)
    return book_result


async def send_results_duration_all_time(message, bot, state):
    book_result = await book_results_duration_all_time(message=message, bot=bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': BestBook}
    await send_results_to_user(information_for_search_books)


async def show_pages_if_they_exist(pages: str, state: FSMContext, message: types.Message):
    if pages:
        await state.update_data(next_page_url=pages)
        await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
        await BestBook.next_page.set()
    else:
        await there_are_no_books(message=message, state=state)


async def attribute_error(message: types.Message, state: FSMContext):
    logger.error('Ошибка AttributeError')
    await message.answer('В ходе поиска возникла ошибка, попробуйте снова.\n'
                         'Для этого пропишите команду /best_book')
    await state.reset_state()
