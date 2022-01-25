from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from request import find_book, find_book_next_page

from loader import dp, bot
from states import FindBook
from keyboard.default.next_page_buttons import choice
from loguru import logger


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
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await FindBook.choice.set()
        else:
            await message.answer('Книг больше нет')
            await state.reset_state()


@logger.catch()
@dp.message_handler(state=FindBook.choice)
async def result(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        logger.info('Бот приступил к открытию следующей страницы в команде /find_book')
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await find_book_next_page(url=data["next_page_url"], message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await FindBook.choice.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Хорошо, поиск книг завершен.\nЧтобы узнать весь функционал введите комманду /help',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await FindBook.choice.set()


