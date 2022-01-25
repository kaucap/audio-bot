from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext

from loader import dp, bot
from states import PaidBook
from keyboard.default.type_of_book_buttons import choose_type
from keyboard.default.next_page_buttons import choice
from request import find_book_next_page, paid_book_new, paid_book_best, paid_book_popular
from loguru import logger


@logger.catch()
@dp.message_handler(Command("paid_book"))
async def looking_new_book(message: types.Message):
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /paid_book')
    await message.answer('Выберите вид книг', reply_markup=choose_type)
    await PaidBook.book.set()


@logger.catch()
@dp.message_handler(state=PaidBook.book)
async def choosing_type_of_book(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Новые 🆕':
        logger.info('Бот приступил к выполнению команды /paid_book')
        await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
        book_result = await paid_book_new(message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await PaidBook.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    elif answer == 'Лучшие 🔥':
        logger.info('Бот приступил к выполнению команды /paid_book')
        await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
        book_result = await paid_book_best(message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await PaidBook.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    elif answer == 'Обсуждаемые 🗣':
        logger.info('Бот приступил к выполнению команды /paid_book')
        await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
        book_result = await paid_book_popular(message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await PaidBook.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов!"')
        await PaidBook.book.set()


@logger.catch()
@dp.message_handler(state=PaidBook.next_page)
async def next_page_book(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        logger.info('Бот приступил к открытию следующей страницы в команде /paid_book')
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await find_book_next_page(url=data["next_page_url"], message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await PaidBook.next_page.set()
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
        await PaidBook.next_page.set()
