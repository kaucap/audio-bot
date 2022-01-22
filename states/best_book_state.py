from aiogram.dispatcher.filters.state import StatesGroup, State


class BestBook(StatesGroup):
    book = State()
    choice = State()
    next_page = State()
