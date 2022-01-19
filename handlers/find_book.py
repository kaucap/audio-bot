from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from request import find_book, next_page
from aiogram.types import CallbackQuery

from loader import dp, bot
from states import FindBook
from keyboard.inline.next_page_buttons import choice


@dp.message_handler(Command("find_book"))
async def choose_book(message: types.Message):
    await message.answer('Введите автора или название книги')
    await FindBook.book.set()


@dp.message_handler(state=FindBook.book)
async def looking_book(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 200:
        await message.answer('Максимально допустимое количество символов - 200. Попробуйте снова')
        await FindBook.book.set()
    else:
        await state.update_data(book=answer)
        await message.answer('Приступаю к поиску')
        data = await state.get_data()
        result = await find_book(answer=data["book"], message=message, bot=bot)
        if result:
            await state.update_data(next_page_url=result)
            await message.answer('Какое действие совершим?', reply_markup=choice)
        else:
            await message.answer('Книг больше нет')
            await state.reset_state()


@dp.callback_query_handler(text="next_page", state=FindBook)
async def new_page(message: types.Message, state: FSMContext):
    await message.answer('Приступаю к поиску')
    data = await state.get_data()
    result = await next_page(url=data["next_page_url"], message=message, bot=bot)
    if result:
        await state.update_data(next_page_url=result)
        await message.answer('Какое действие совершим?', reply_markup=choice)
    else:
        await message.answer('Книг больше нет')
        await state.reset_state()


@dp.callback_query_handler(text="cancel", state=FindBook)
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer("Вы отменили текущую комманду")
    await call.message.edit_reply_markup()
    await call.message.answer('Для просмотра всего функционала, воспользуйтесь коммандой /help')
    await state.reset_state()
