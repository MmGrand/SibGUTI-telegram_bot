from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск преподавателя"),
            KeyboardButton(text="Список расписаний")
        ],
        [
            KeyboardButton(text="Информация о институтах"),
            KeyboardButton(text="Социальные сети СибГУТИ")
        ],
        [
            KeyboardButton(text="Дополнительные увлечения"),
            KeyboardButton(text="Общежития")
        ],
    ],
    resize_keyboard=True
)


dormitories = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1 общежитие"),
            KeyboardButton(text="2 общежитие")
        ],
        [
            KeyboardButton(text="3 общежитие"),
            KeyboardButton(text="4 общежитие")
        ],
        [
            KeyboardButton(text="Назад"),
        ],
    ],
    resize_keyboard=True
)
