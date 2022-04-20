import bs4
from aiogram.types import ReplyKeyboardRemove
from loguru import logger
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import aiogram
from request import paid_book_new, paid_book_best, paid_book_popular
from states import PaidBook
from utils.book_information import if_search_results_have_pages
from utils.handlers.common import send_results_to_user


async def paid_book_results_new(message: types.Message, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /paid_book')
    await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
    book_result = await paid_book_new(message=message, bot=bot)
    return book_result


async def send_paid_book_results_new(message: types.Message, state: FSMContext, bot: aiogram.Bot):
    book_result = await paid_book_results_new(message, bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': PaidBook}
    await send_results_to_user(information_for_search_books)


async def paid_book_results_best(message: types.Message, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /paid_book')
    await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
    book_result = await paid_book_best(message=message, bot=bot)
    return book_result


async def send_paid_book_results_best(message: types.Message, state: FSMContext, bot: aiogram.Bot):
    book_result = await paid_book_results_best(message, bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': PaidBook}
    await send_results_to_user(information_for_search_books)


async def paid_book_results_popular(message: types.Message, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /paid_book')
    await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
    book_result = await paid_book_popular(message=message, bot=bot)
    return book_result


async def send_paid_book_results_popular(message: types.Message, state: FSMContext, bot: aiogram.Bot):
    book_result = await paid_book_results_popular(message, bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': PaidBook}
    await send_results_to_user(information_for_search_books)
