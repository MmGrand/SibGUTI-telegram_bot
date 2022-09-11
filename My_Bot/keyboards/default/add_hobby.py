from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

add_hobby = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Студенческие отряды"),
            KeyboardButton(text="Фестивали")
        ],
        [
            KeyboardButton(text="Профсоюз студентов"),
            KeyboardButton(text="Студклуб")
        ],
        [
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True,
)


stud_squads = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отряды проводников"),
            KeyboardButton(text="Вожатские отряды")
        ],
        [
            KeyboardButton(text="Строительные отряды"),
            KeyboardButton(text="Сервисные отряды")
        ],
        [
            KeyboardButton(text="Сельскохозяйственные отряды"),
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True,
)


festivals = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Фестиваль ИВТ"),
            KeyboardButton(text="Фестиваль МРМ")
        ],
        [
            KeyboardButton(text="Фестиваль МТС"),
            KeyboardButton(text="Фестиваль ГФ")
        ],
        [
            KeyboardButton(text="Фестиваль АЭС"),
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True,
)


stud_club = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Народный коллектив академический хор им. В. Серебровского"),
            KeyboardButton(text="Народный коллектив стиль-балет «Единое дыхание»")
        ],
        [
            KeyboardButton(text="Вокальный джаз-ансамбль «Волярэ»"),
            KeyboardButton(text="Мужской вокальный ансамбль «Септима»")
        ],
        [
            KeyboardButton(text="Женский вокальный ансамбль «Синкопа»"),
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True,
)


trade_union = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Основное про профсоюз")
        ],
        [
            KeyboardButton(text="Социальные сети")
        ],
        [
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard=True,
)
