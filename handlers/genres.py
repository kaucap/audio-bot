from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from keyboard.default.genres_buttons import genres
from keyboard.default.type_of_book_buttons import choose_type
from loader import dp, bot
from states import Genres
from utils.handlers.common import clear_user_history_if_reach_limit, user_wants_see_next_page
from utils.handlers.genres import send_book_new, send_book_best, send_book_discussed


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
        data = await state.get_data()
        request = f'Поиск книги по жанру: {data["genre"]}'
        await clear_user_history_if_reach_limit(message=message, request=request)
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
        await send_book_new(message=message, state=state, bot=bot)
    elif answer == 'Лучшие 🔥':
        await send_book_best(message=message, state=state, bot=bot)
    elif answer == 'Обсуждаемые 🗣':
        await send_book_discussed(message=message, state=state, bot=bot)
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов!"')
        await Genres.choose_type.set()


@logger.catch()
@dp.message_handler(state=Genres.next_page)
async def next_page_book(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        current_command = 'genres'
        information_for_search_books = {'command': current_command, 'message': message, 'state': state,
                                        'bot': bot, 'current_state': Genres}
        await user_wants_see_next_page(information_for_search_books)
    elif answer == "Нет ❌" or answer == "Нет":
        await message.answer('Хорошо, поиск книг завершен.\nЧтобы узнать весь функционал введите комманду /help',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВведите "Да" или "Нет"')
        await Genres.next_page.set()
