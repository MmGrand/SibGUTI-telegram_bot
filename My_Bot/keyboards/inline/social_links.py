from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инлайн клавиатура соц сетей СибГУТИ
urlKeyboard = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text="Инстаграмм", url="https://www.instagram.com/sibguti/?hl=ru")
urlButton2 = InlineKeyboardButton(text="Вконтакте", url="https://vk.com/sibguti_info")
urlButton3 = InlineKeyboardButton(text="Youtube", url="https://www.youtube.com/channel/UCf0W3kmAfTYbCkfL1C56Ozg")
urlButton4 = InlineKeyboardButton(text="Телеграмм", url="https://t.me/sibsutis_info")
urlKeyboard.add(urlButton, urlButton2, urlButton3, urlButton4)

# Инлайн клавиатура расписания
schedule_Keyboard = InlineKeyboardMarkup(row_width=1)
sch_Button = InlineKeyboardButton(text="Расписание занятий студентов", url="https://sibsutis.ru"
                                                                           "/students/schedule/")
sch_Button2 = InlineKeyboardButton(text="Расписание занятий преподавателей", url="https://sibsutis.ru/students/schedule"
                                                                                 "/?type=teacher")
sch_Button3 = InlineKeyboardButton(text="Расписание занятий по аудиториям", url="https://sibsutis.ru/students/"
                                                                                "schedule/?type=room")
schedule_Keyboard.add(sch_Button, sch_Button2, sch_Button3)
