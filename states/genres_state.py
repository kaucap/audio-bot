from aiogram.dispatcher.filters.state import StatesGroup, State


class Genres(StatesGroup):
    choice = State()
    next_page = State()
    choose_type = State()
