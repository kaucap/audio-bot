from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext

from db_api.schemas.user_request import Info
from request import find_new_book, find_book_next_page

from loader import dp, bot
from states import FindNewBook
from keyboard.default.next_page_buttons import choice
from loguru import logger
from db_api import sql_commands as command


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
        search_book_info = await command.choose_info(user_id=message.from_user.id)
        request = 'Поиск новых книг'
        if len(search_book_info) >= 20:
            await Info.delete.where(message.from_user.id == Info.id).gino.status()
        await command.add_info(id=message.from_user.id, request=request)
        logger.info('Бот приступил к выполнению команды /new_book')
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        book_result = await find_new_book(message=message, bot=bot)
        try:
            if book_result:
                await state.update_data(next_page_url=book_result)
                await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
                await FindNewBook.choice.set()
            else:
                await message.answer('Книг больше нет')
                await state.reset_state()
        except AttributeError:
            logger.error('Ошибка AttributeError')
            await message.answer('В ходе поиска возникла ошибка, попробуйте снова.\n'
                                 'Для этого пропишите команду /new_book')
            await state.reset_state()
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Вы отменили поиск книг. Для ознакомления со всем функционалом '
                             'бота введите /help', reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await FindNewBook.book.set()


@logger.catch()
@dp.message_handler(state=FindNewBook.choice)
async def result(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        logger.info('Бот приступил к открытию следующей страницы в команде /new_book')
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await find_book_next_page(url=data["next_page_url"], message=message, bot=bot)
        try:
            if book_result:
                await state.update_data(next_page_url=book_result)
                await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
                await FindNewBook.choice.set()
            else:
                await message.answer('Книг больше нет')
                await state.reset_state()
        except AttributeError:
            logger.error('Ошибка AttributeError')
            await message.answer('В ходе поиска возникла ошибка, попробуйте снова.\n'
                                 'Для этого пропишите команду /new_book')
            await state.reset_state()
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Хорошо, поиск книг завершен.\nЧтобы узнать весь функционал введите комманду /help',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await FindNewBook.choice.set()
