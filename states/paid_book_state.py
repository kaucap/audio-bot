from aiogram.dispatcher.filters.state import StatesGroup, State


class PaidBook(StatesGroup):
    book = State()
    choice = State()
    next_page = State()
