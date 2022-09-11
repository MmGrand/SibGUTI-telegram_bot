from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

institutes = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Институт телекоммуникаций"),
            KeyboardButton(text="Институт базовых дисциплин")
        ],
        [
            KeyboardButton(text="Институт информатики и вычислительной техники")
        ],
        [
            KeyboardButton(text="Институт заочного образования")
        ],
[
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True
)


info_institute_bd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Кафедры"),
            KeyboardButton(text="Контакты")
        ],
        [
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True
)

info_institute_zo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Направления бакалавриата"),
            KeyboardButton(text="Минимальные баллы ЕГЭ")
        ],
        [
            KeyboardButton(text="Направления магистратуры"),
        ],
        [
            KeyboardButton(text="Контакты"),
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True
)

info_institutes = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Кафедры"),
            KeyboardButton(text="Контакты")
        ],
        [
            KeyboardButton(text="Направления бакалавриата"),
            KeyboardButton(text="Минимальные баллы ЕГЭ")
        ],
        [
            KeyboardButton(text="Направления магистратуры"),
        ],
        [
            KeyboardButton(text="Направления специалитета"),
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True
)
