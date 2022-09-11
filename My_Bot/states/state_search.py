from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


class SearchInst(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()


class SearchHobby(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()


class SearchDormitory(StatesGroup):
    Q1 = State()
