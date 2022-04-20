import aiogram
import bs4
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from request import new_book_by_genre, best_book_by_genre, popular_book_by_genre
from states import Genres
from utils.book_information import if_search_results_have_pages
from utils.handlers.common import send_results_to_user


async def find_book_new(message: types.Message, state: FSMContext, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /genres')
    await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    book_result = await new_book_by_genre(message=message, bot=bot, data=data)
    return book_result


async def send_book_new(message: types.Message, state: FSMContext, bot: aiogram.Bot):
    book_result = await find_book_new(message=message, state=state, bot=bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': Genres}
    await send_results_to_user(information_for_search_books)


async def find_book_best(message: types.Message, state: FSMContext, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /genres')
    await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    book_result = await best_book_by_genre(message=message, bot=bot, data=data)
    return book_result


async def send_book_best(message: types.Message, state: FSMContext, bot: aiogram.Bot):
    book_result = await find_book_best(message=message, state=state, bot=bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': Genres}
    await send_results_to_user(information_for_search_books)


async def find_book_discussed(message: types.Message, state: FSMContext, bot: aiogram.Bot) -> bs4.BeautifulSoup:
    logger.info('Бот приступил к выполнению команды /genres')
    await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    book_result = await popular_book_by_genre(message=message, bot=bot, data=data)
    return book_result


async def send_book_discussed(message: types.Message, state: FSMContext, bot: aiogram.Bot):
    book_result = await find_book_discussed(message=message, state=state, bot=bot)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': Genres}
    await send_results_to_user(information_for_search_books)
