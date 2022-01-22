from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from request import find_book_next_page, best_book_day, best_book_week, best_book_month, best_book_all_time

from loader import dp, bot
from states import BestBook
from keyboard.default.period_of_time_buttons import choose_time
from keyboard.default.next_page_buttons import choice


@dp.message_handler(Command("best_book"))
async def looking_new_book(message: types.Message):
    await message.answer('Выберите за какой промежуток времени мне вывести лучшие книги?', reply_markup=choose_time)
    await BestBook.choice.set()


@dp.message_handler(state=BestBook.choice)
async def choosing_time(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'День':
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        await best_book_day(message=message, bot=bot)
        await message.answer('Книг больше нет')
        await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
        await state.reset_state()
    elif answer == 'Неделя':
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        book_result = await best_book_week(message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await BestBook.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    elif answer == 'Месяц':
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        book_result = await best_book_month(message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await BestBook.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    elif answer == 'За всё время':
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        book_result = await best_book_all_time(message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await BestBook.next_page.set()
        else:
            await message.answer('Книг больше нет')
            await message.answer('Для того чтобы посмотреть список возможных команд введите /help')
            await state.reset_state()
    else:
        await message.answer('Вы ввели неверный промежуток времени, попробуйте снова!')
        await BestBook.choice.set()


@dp.message_handler(state=BestBook.next_page)
async def next_page(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == "Да ✅" or answer == "Да":
        await message.answer('Хорошо, сейчас покажу книги', reply_markup=ReplyKeyboardRemove())
        data = await state.get_data()
        book_result = await find_book_next_page(url=data["next_page_url"], message=message, bot=bot)
        if book_result:
            await state.update_data(next_page_url=book_result)
            await message.answer('Показать книги со следующей страницы?', reply_markup=choice)
            await BestBook.next_page.set()
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
        await BestBook.next_page.set()
