from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

search_teachers = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск по фио")
        ],
        [
            KeyboardButton(text="Поиск только по фамилии")
        ],
        [
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True,
)
