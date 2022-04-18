from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from loader import dp, bot
from request import find_book
from states import FindBook
from utils.book_information import if_search_results_have_pages
from utils.handlers.common import clear_user_history_if_reach_limit, send_results_to_user, user_wants_see_next_page


@logger.catch()
@dp.message_handler(Command("find_book"))
async def choose_book(message: types.Message):
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /find_book')
    await message.answer('Введите автора или название книги')
    await FindBook.book.set()


@logger.catch()
@dp.message_handler(state=FindBook.book)
async def looking_book(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 200:
        await message.answer('Максимально допустимое количество символов - 200. Попробуйте снова')
        await FindBook.book.set()
    else:
        await state.update_data(book=answer)
        await message.answer('Приступаю к поиску')
        logger.info('Бот приступил к выполнению команды /find_book')
        data = await state.get_data()
        book_result = await find_book(answer=data["book"], message=message, bot=bot)
        request = f'Поиск книги или автора под названием: {data["book"]}'
        await clear_user_history_if_reach_limit(message=message, request=request)
        pages = await if_search_results_have_pages(book_result)
        information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': FindBook}
        await send_results_to_user(information_for_search_books)


@logger.catch()
@dp.message_handler(state=FindBook.next_page)
async def result(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        current_command = 'find_book'
        information_for_search_books = {'command': current_command, 'message': message, 'state': state,
                                        'bot': bot, 'current_state': FindBook}
        await user_wants_see_next_page(information_for_search_books)
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Хорошо, поиск книг завершен.\nЧтобы узнать весь функционал введите комманду /help',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await FindBook.next_page.set()
