from aiogram.dispatcher.filters.state import StatesGroup, State


class FindNewBook(StatesGroup):
    book = State()
    choice = State()
    next_page = State()
