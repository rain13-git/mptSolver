from aiogram.dispatcher.filters.state import StatesGroup, State


class Subject(StatesGroup):
    ref = State()
    file = State()
    price = State()
    description = State()
    cancellation = State()
    menu = State()


class Admin(StatesGroup):
    price = State()
    solve = State()