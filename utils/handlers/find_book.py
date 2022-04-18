from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from keyboard.default.next_page_buttons import choice
from states import FindBook


async def show_pages_if_they_exist(pages: str, state: FSMContext, message: types.Message):
    if pages:
        await state.update_data(next_page_url=pages)
        await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
        await FindBook.next_page.set()
    else:
        await message.answer('Книг больше нет')
        await state.reset_state()


async def attribute_error(message: types.Message, state: FSMContext):
    logger.error('Ошибка AttributeError')
    await message.answer('В ходе поиска возникла ошибка, попробуйте снова.\n'
                         'Для этого пропишите команду /find_book')
    await state.reset_state()


async def send_results_to_user(pages: str, state: FSMContext, message: types.Message):
    try:
        await show_pages_if_they_exist(pages=pages, state=state, message=message)
    except AttributeError:
        await attribute_error(message=message, state=state)
