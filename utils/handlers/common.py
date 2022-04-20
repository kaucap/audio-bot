import bs4
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from db_api import sql_commands as command
from db_api.schemas.user_request import Info
from keyboard.default.next_page_buttons import choice
from request import find_book_next_page
from utils.book_information import if_search_results_have_pages


async def there_are_no_books(message: types.Message, state: FSMContext):
    await message.answer('Книг больше нет')
    await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
    await state.reset_state()


async def clear_user_history_if_reach_limit(message: types.Message, request: str):
    search_book_info = await command.choose_info(user_id=message.from_user.id)
    if len(search_book_info) >= 20:
        await Info.delete.where(message.from_user.id == Info.id).gino.status()
    await command.add_info(id=message.from_user.id, request=request)


async def show_pages_if_they_exist(information_for_search_books: dict):
    pages = information_for_search_books['pages']
    state = information_for_search_books['state']
    message = information_for_search_books['message']
    current_state = information_for_search_books['current_state']
    if pages:
        await state.update_data(next_page_url=pages)
        await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
        await current_state.next_page.set()
    else:
        await message.answer('Книг больше нет')
        await state.reset_state()


async def attribute_error(information_for_search_books: dict):
    message = information_for_search_books['message']
    state = information_for_search_books['state']
    logger.error('Ошибка AttributeError')
    await message.answer('В ходе поиска возникла ошибка, попробуйте снова.\n'
                         'Для этого пропишите команду /find_book')
    await state.reset_state()


async def send_results_to_user(information_for_search_books: dict):
    try:
        await show_pages_if_they_exist(information_for_search_books)
    except AttributeError:
        await attribute_error(information_for_search_books)


async def show_books_from_next_page(information_for_search_books: dict) -> bs4.BeautifulSoup:
    current_command = information_for_search_books['command']
    message = information_for_search_books['message']
    state = information_for_search_books['state']
    bot = information_for_search_books['bot']

    logger.info(f'Бот приступил к открытию следующей страницы в команде /{current_command}')
    await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    book_result = await find_book_next_page(url=data["next_page_url"], message=message, bot=bot)
    return book_result


async def user_wants_see_next_page(information_for_search_books: dict):
    current_command = information_for_search_books['command']
    message = information_for_search_books['message']
    state = information_for_search_books['state']
    bot = information_for_search_books['bot']
    current_state = information_for_search_books['current_state']
    information_for_search_books_next_page = {'message': message, 'state': state, 'bot': bot,
                                              'command': current_command}
    book_result = await show_books_from_next_page(information_for_search_books_next_page)
    pages = await if_search_results_have_pages(book_result)
    information_for_search_books = {'pages': pages, 'state': state, 'message': message, 'current_state': current_state}
    await send_results_to_user(information_for_search_books)
