from aiogram.dispatcher.filters.state import StatesGroup, State


class FindBook(StatesGroup):
    book = State()
    result = State()
    next_page = State()
