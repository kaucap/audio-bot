from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from request import new_book_by_genre, best_book_by_genre, popular_book_by_genre, find_book_next_page

from loader import dp, bot
from states import Genres
from keyboard.default.next_page_buttons import choice
from keyboard.default.genres_buttons import genres
from keyboard.default.type_of_book_buttons import choose_type
from loguru import logger


@logger.catch()
@dp.message_handler(Command('genres'))
async def choosing_genre(message: types.Message):
    logger.info(f'Клиент с id: {message.from_user.id} запустил команду /genres')
    await message.answer('Выберите один из жанров', reply_markup=genres)
    await Genres.choice.set()


@logger.catch()
@dp.message_handler(state=Genres.choice)
async def choosing_type_of_book(message: types.Message, state: FSMContext):
    genre_types = ['Фантастика 🛸', 'Детективы 🕵️‍♂️', 'Роман ❤️', 'Психология 📚', 'Классика ✨', 'Ужасы 👀']
    answer = message.text
    if answer in genre_types:
        await state.update_data(genre=answer)
        await message.answer('Хорошо, выберите вид книг', reply_markup=choose_type)
        await Genres.choose_type.set()
    else:
        await message.answer('Вы ввели неправильный жанр, попробуйте снова!')
        await Genres.choice.set()


@logger.catch()
@dp.message_handler(state=Genres.choose_type)
async def result(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Новые 🆕':
        logger.info('Бот приступил к выполнению команды /genres')
        await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await new_book_by_genre(message=message, bot=bot, data=data)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await Genres.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    elif answer == 'Лучшие 🔥':
        logger.info('Бот приступил к выполнению команды /genres')
        await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await best_book_by_genre(message=message, bot=bot, data=data)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await Genres.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    elif answer == 'Обсуждаемые 🗣':
        logger.info('Бот приступил к выполнению команды /genres')
        await message.answer('Хорошо, приступаю к поиску', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await popular_book_by_genre(message=message, bot=bot, data=data)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await Genres.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов!"')
        await Genres.choose_type.set()


@logger.catch()
@dp.message_handler(state=Genres.next_page)
async def next_page_book(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        logger.info('Бот приступил к открытию следующей страницы в команде /genres')
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await find_book_next_page(url=data["next_page_url"], message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await Genres.next_page.set()
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
        await Genres.next_page.set()
