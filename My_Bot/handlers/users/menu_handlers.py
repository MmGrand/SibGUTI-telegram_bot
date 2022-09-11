from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from keyboards.default.start_menu import start_menu, dormitories
from keyboards.default.institutes import institutes, info_institutes, info_institute_bd, info_institute_zo
from keyboards.default.teachers import search_teachers
from keyboards.default.add_hobby import add_hobby, stud_squads, festivals, trade_union, stud_club
from keyboards.inline.social_links import urlKeyboard, schedule_Keyboard
from states.state_search import Search, SearchInst, SearchHobby, SearchDormitory
from utils.db_api import helper_Sibguti_db

from loader import dp, bot


# Команда отмены
@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Отмена действий прошла успешно!", reply_markup=ReplyKeyboardRemove())


# Кнопка возврата
@dp.message_handler(state="*", commands='back')
@dp.message_handler(Text(equals="Назад", ignore_case=True), state="*")
async def back_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    if current_state == 'SearchInst:Q1' or current_state == 'Search:Q1' or current_state == 'Search:Q2' or \
            current_state == 'Search:Q3' or current_state == 'SearchHobby:Q1' or current_state == 'SearchDormitory:Q1':
        await state.finish()
        await show_menu(message)
    elif current_state == 'SearchInst:Q2' or current_state == 'SearchInst:Q3' or current_state == 'SearchInst:Q4' or \
            current_state == 'SearchInst:Q5':
        await state.finish()
        await info_institute(message)
    elif current_state == 'SearchHobby:Q2' or current_state == 'SearchHobby:Q3' or current_state == 'SearchHobby:Q4' \
            or current_state == 'SearchHobby:Q5':
        await state.finish()
        await info_hobby(message)


# Команда меню
@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите о чём или о ком хотите узнать:", reply_markup=start_menu)


# Получение ссылок на социальные сети
@dp.message_handler(Text("Социальные сети СибГУТИ"))
async def get_social_links(message: Message):
    await message.answer(f"Социальные сети СибГУТИ:", reply_markup=urlKeyboard)


# Получении пока что ссылки на сайт с расписаниями
@dp.message_handler(Text("Список расписаний"))
async def search_schedule(message: Message):
    await message.answer("Тут можно узнать о:\n"
                         "📍Расписаний групп, на которые вы хотите поступать.\n"
                         "📍Расписаний преподавателей, которых вы уже увидели в своём будущем учебном плане.\n"
                         "📍Расписаний аудиторий. Вдруг вы уже были в какой-то аудитории и хотите посмотреть "
                         "есть ли шанс учиться вам именно в ней."
                         "", reply_markup=schedule_Keyboard)


# Поиск преподавателя
@dp.message_handler(Text("Поиск преподавателя"))
async def search_teacher(message: Message):
    await message.answer("Выберите нужный вариант:", reply_markup=search_teachers)
    await Search.Q1.set()


# Поиск преподавателя по фио
@dp.message_handler(Text("Поиск по фио"), state=Search.Q1)
async def input_fio(message: Message):
    await message.answer("Введите фио полностью:")
    await Search.Q2.set()


@dp.message_handler(state=Search.Q2)
async def search_fio(message: Message):
    await helper_Sibguti_db.sql_search(message)
    await Search.Q1.set()


# Поиск преподавателей по фамилии, может быть несколько человек
@dp.message_handler(Text("Поиск только по фамилии"), state=Search.Q1)
async def input_lastname(message: Message):
    await message.answer("Введите фамилию преподавателя:")
    await Search.Q3.set()


@dp.message_handler(state=Search.Q3)
async def search_lastname(message: Message):
    await helper_Sibguti_db.sql_search_lastname(message)
    await Search.Q1.set()


# Вывод информации о институтах
@dp.message_handler(Text("Информация о институтах"))
async def info_institute(message: Message):
    await message.answer("Выберите институт, о котором хотите узнать поподробнее:", reply_markup=institutes)
    await SearchInst.Q1.set()


# Информация о институте базовых дисциплин
@dp.message_handler(Text("Институт базовых дисциплин"), state=SearchInst.Q1)
async def institute_bd(message: Message):
    await message.answer(f"📌Институт базовых дисциплин создан в 2021 году. Он объединил кафедры, обеспечивающие "
                         f"преподавание фундаментальных дисциплин студентам всех направлений.\n📌Задача Института – "
                         f"формирование плодотворной интеллектуальной и творческой атмосферы и развитие общего "
                         f"академического кругозора студентов.\nЧто хотите о нём узнать?",
                         reply_markup=info_institute_bd)
    await SearchInst.Q2.set()


@dp.message_handler(Text("Кафедры"), state=SearchInst.Q2)
async def department_bd(message: Message):
    await message.answer(f"Всю основную информацию о кафедрах можно узнать по ссылкам:\n"
                         f"📌Кафедра высшей математики: https://sibsutis.ru/institutes/ibasic/124187/\n"
                         f"📌Кафедра физического воспитания: https://sibsutis.ru/institutes/ibasic/124192/\n"
                         f"📌Кафедра физики:\nhttps://sibsutis.ru/institutes/ibasic/124190/\n"
                         f"📌Кафедра иностранных и русского языков: https://sibsutis.ru/institutes/ibasic/124191/\n"
                         f"📌Кафедра философии и истории: https://sibsutis.ru/institutes/ibasic/124193/"
                         f"", disable_web_page_preview=True)


@dp.message_handler(Text("Контакты"), state=SearchInst.Q2)
async def contacts_bd(message: Message):
    await message.answer(f"📌Страница в Вконтакте: https://vk.com/sibsutis_baza"
                         , disable_web_page_preview=True)


# Информация о институте информатики и вычислительной техники
@dp.message_handler(Text("Институт информатики и вычислительной техники"), state=SearchInst.Q1)
async def institute_ivt(message: Message):
    await message.answer(f"📌Институт информатики и вычислительной техники (ИВТ) был образован в 2021 в результате "
                         f"объединения выпускающих кафедр факультета информатики и вычислительной техники (ИВТ), "
                         f"гуманитарного факультета (ГФ), а также кафедры безопасности и управления в телекоммуникациях"
                         f" (БиУТ).\nЧто хотите о нём узнать?", reply_markup=info_institutes)
    await SearchInst.Q3.set()


@dp.message_handler(Text("Кафедры"), state=SearchInst.Q3)
async def department_ivt(message: Message):
    await message.answer(f"Всю основную информацию о кафедрах можно узнать по ссылкам:\n"
                         f"📌Кафедра безопасности и управления в телекоммуникациях: "
                         f"https://sibsutis.ru/institutes/iivt/124207/\n"
                         f"📌Кафедра вычислительных систем: https://sibsutis.ru/institutes/iivt/124186/\n"
                         f"📌Кафедра математического моделирования и цифрового развития бизнес систем: "
                         f"https://sibsutis.ru/institutes/iivt/124189/\n"
                         f"📌Кафедра социально-коммуникативных технологий: https://sibsutis.ru/institutes/iivt/124208/\n"
                         f"📌Кафедра прикладной математики и кибернетики: https://sibsutis.ru/institutes/iivt/124195/\n"
                         f"📌Кафедра телекоммуникационных систем и вычислительных средств: "
                         f"https://sibsutis.ru/institutes/iivt/124188/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Направления бакалавриата"), state=SearchInst.Q3)
async def direction_bk_ivt(message: Message):
    await message.answer(f"Список направлений бакалавриата:\n"
                         f"1) 01.03.02 Прикладная математика и информатика\n"
                         f"2) 02.03.02 Фундаментальная информатика и информационные технологии\n"
                         f"3) 09.03.01 Информатика и вычислительная техника\n"
                         f"4) 09.03.03 Прикладная информатика\n"
                         f"5) 10.03.01 Информационная безопасность\n"
                         f"6) 38.03.05 Бизнес-информатика\n"
                         f"7) 42.03.01 Реклама и связи с общественностью\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes/iivt/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Направления магистратуры"), state=SearchInst.Q3)
async def direction_mg_ivt(message: Message):
    await message.answer(f"Список направлений магистратуры:\n"
                         f"1) 09.04.01 Информатика и вычислительная техника\n"
                         f"2) 09.04.03 Прикладная информатика в экономике\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes/iivt/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Направления специалитета"), state=SearchInst.Q3)
async def direction_sp_ivt(message: Message):
    await message.answer(f"Список направлений специалитета:\n"
                         f"1) 10.05.02 Информационная безопасность телекоммуникационных систем\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes/iivt/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Контакты"), state=SearchInst.Q3)
async def contacts_ivt(message: Message):
    await message.answer(f"📌И.о. директора – к.т.н., доцент Приставка Павел Анатольевич, каб. 615а корпус 1, "
                         f"73832698271, ppa@sibguti.ru\n"
                         f"📌Зам. директора по учебной работе – к.ф.н., доцент Карев Евгений Иванович, каб. 623 корпус "
                         f"1,73832698362, evg-kareff@yandex.ru\n"
                         f"📌Зам. директора по воспитательной работе – к.ф.н., доцент Логутова Марина Алексеевна, каб. "
                         f"623 корпус 1, 73832698362, loguter@inbox.ru\n"
                         f"📌Специалисты по работе со студентами:\n"
                         f"📌Штанке Татьяна Васильевна, каб. 622 корпус 1, 73832698270,  ivt@sibguti.ru\n"
                         f"📌Лапоногова Алина Эдуардовна, каб. 622 корпус 1, 73832698270, alinaky@mail.ru\n"
                         f"📌Франке Елена Анатольевна каб. 622 корпус 1, 73832698271\n"
                         f"📌Telegram-канал института ИВТ: https://t.me/ivtsibsutis\n"
                         f"📌Страница в вконтакте: https://vk.com/ivtsibsutis"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Минимальные баллы ЕГЭ"), state=SearchInst.Q3)
async def scores_ivt(message: Message):
    await message.answer(f"📌10.03.01 Информационная безопасность (информатика/физика + математика + русский язык):\n"
                         f"Бюджет - 213 баллов\nВнебюджет - 115 баллов\nОсобое право - 155 баллов\n"
                         f"📌09.03.01 Информатика и вычислительная техника (информатика/физика + математика + русский"
                         f" язык)\nБюджет - 202 баллов\nВнебюджет - 115 баллов\nОсобое право - 134 баллов\nЦелевой "
                         f"приём - 105 баллов\n"
                         f"📌09.03.03 Прикладная информатика (информатика/физика + математика + русский язык):\n"
                         f"Бюджет - 193 баллов\nВнебюджет - 129 баллов\nОсобое право - 192 баллов\nЦелевой приём - "
                         f"169 баллов\n"
                         f"📌02.03.02 Фундаментальная информатика и информационные технологии (информатика/физика "
                         f"+ математика + русский язык):\nБюджет - 205 баллов\nВнебюджет - 131 баллов\n"
                         f"📌РСО-внебюджет, направление 42.03.01 - 126 баллов (история/информатика + обществознание "
                         f"+ русский язык)\n📌БИ-внебюджет, направление 38.03.05 - 140 баллов (математика + "
                         f"обществознание/информатика + русский язык)")


# Информация о институте телекоммуникаций
@dp.message_handler(Text("Институт телекоммуникаций"), state=SearchInst.Q1)
async def institute_t(message: Message):
    await message.answer(f"📌Институт телекоммуникаций (ИТ) был образован в 2021 году в результате слияния трех крупных "
                         f"факультетов СибГУТИ – факультета Автоматической электросвязи (АЭС), факультета "
                         f"мультисервисных телекоммуникационных систем (МТС) и факультета мобильной радиосвязи и "
                         f"мультимедиа (МРМ).\n📌Сфера интересов института телекоммуникаций охватывает все направления "
                         f"развития современных инфокоммуникаций, вопросов архитектуры, оптимизации и проектирования "
                         f"проводных и беспроводных систем и сетей связи, цифрового телерадиовещания."
                         f"\nЧто хотите о нём узнать?", reply_markup=info_institutes)
    await SearchInst.Q4.set()


@dp.message_handler(Text("Кафедры"), state=SearchInst.Q4)
async def department_t(message: Message):
    await message.answer(f"Всю основную информацию о кафедрах можно узнать по ссылкам:\n"
                         f"📌Кафедра инфокоммуникационных систем и сетей: "
                         f"https://sibsutis.ru/institutes/itelecom/124205/\n"
                         f"📌Кафедра радиотехнических систем: https://sibsutis.ru/institutes/itelecom/124197/\n"
                         f"📌Кафедра радиотехнических устройств и техносферной безопасности: "
                         f"https://sibsutis.ru/institutes/itelecom/124199/\n"
                         f"📌Кафедра систем автоматизированного проектирования: https://sibsutis.ru/institutes/itelecom"
                         f"/124196/\n"
                         f"📌Кафедра технической электроники: https://sibsutis.ru/institutes/itelecom/124198/\n"
                         f"📌Кафедра фотоники в телекоммуникациях: "
                         f"https://sibsutis.ru/institutes/itelecom/124200/\n"
                         f"📌Кафедра цифрового телерадиовещания и систем радиосвязи: "
                         f"https://sibsutis.ru/institutes/itelecom/124206/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Направления бакалавриата"), state=SearchInst.Q4)
async def direction_bk_t(message: Message):
    await message.answer(f"Список направлений бакалавриата:\n"
                         f"1) 09.03.02 Информационные системы и технологии\n"
                         f"2) 11.03.01 Радиотехника\n"
                         f"3) 11.03.02 Инфокоммуникационные технологии и системы связи\n"
                         f"4) 11.03.03 Конструирование и технология электронных средств\n"
                         f"5) 11.03.04 Электроника и наноэлектроника\n"
                         f"6) 20.03.01 Техносферная безопасность\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes/"
                         f"itelecom/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Направления магистратуры"), state=SearchInst.Q4)
async def direction_mg_t(message: Message):
    await message.answer(f"Список направлений магистратуры:\n"
                         f"1) 11.04.01 Радиотехника\n"
                         f"2) 11.04.02 Инфокоммуникационные технологии и системы связи\n"
                         f"3) 11.04.03 Конструирование и технология электронных средств\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes/"
                         f"itelecom/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Направления специалитета"), state=SearchInst.Q4)
async def direction_sp_t(message: Message):
    await message.answer(f"Список направлений специалитета:\n"
                         f"1) 11.05.01 Радиоэлектронные системы и комплексы\n"
                         f"2) 11.05.02 Специальные радиотехнические системы\n"
                         f"3) 11.05.04 Инфокоммуникационные технологии и системы специальной связи\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes/"
                         f"itelecom/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Контакты"), state=SearchInst.Q4)
async def contacts_t(message: Message):
    await message.answer(f"📌И.о. директора Шевнина Ирина Евгеньевна, к.т.н., доцент, локация - кабинет 262 (корпус 3),"
                         f" телефон 269-82-44 e-mail: shevnina@sibguti.ru\n"
                         f"📌Заместитель директора по учебной работе Елистратова Ирина Борисовна, локация - "
                         f"кабинет 261 (корпус 3), телефон 269-82-51 e-mail: Irina_Borisovna@bk.ru\n"
                         f"📌Заместитель директора по воспитательной работе Соломина Елена Геннадьевна локация - "
                         f"кабинет 261 (корпус 3), телефон 269-82-51 e-mail: solominaeg@yandex.ru\n"
                         f"📌Дирекция (Специалисты по работе со студентами): локация - кабинет 453 (корпус 3), "
                         f"телефон 269-82-41, e-mail: telecom@sibguti.ru\n"
                         f"📌Зарипова Юлия Владимировна (https://vk.com/aesdekanat)\n"
                         f"📌Гватуа Анна Геннадьевна (https://vk.com/id531848129)\n"
                         f"📌Барабанова Наталья Васильевна (https://vk.com/id170104052)\n"
                         f"📌Страница в вконтакте: https://vk.com/telecom_sibguti"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Минимальные баллы ЕГЭ"), state=SearchInst.Q4)
async def scores_t(message: Message):
    await message.answer(f"📌09.03.02 Информационные системы и технологии (информатика/физика + математика + "
                         f"русский язык):\nБюджет - 209 баллов\nВнебюджет - 105 баллов\nОсобое право - 148 баллов"
                         f"\nЦелевой приём - 153\n"
                         f"📌11.05.04 Инфокоммуникационные технологии и системы специальной связи (информатика/физика"
                         f" + математика + русский язык):\n"
                         f"Бюджет - 159 баллов\nОсобое право - 103 баллов\nЦелевой приём-УВЦ - 131\n"
                         f"📌11.05.01 Радиоэлектронные системы и комплексы (информатика/физика"
                         f" + математика + русский язык):\n"
                         f"Бюджет - 134 баллов\nЦелевой приём-УВЦ - 139\n"
                         f"📌11.05.02 Специальные радиотехнические системы (информатика/физика"
                         f" + математика + русский язык):\n"
                         f"Бюджет - 139 баллов\n"
                         f"📌11.03.00 электроника, радиотехника и системы связи (информатика/физика + математика + "
                         f"русский язык):\n"
                         f"Бюджет - 105 баллов\nВнебюджет - 126 баллов")


# Информация о институте заочного образования
@dp.message_handler(Text("Институт заочного образования"), state=SearchInst.Q1)
async def institute_zo(message: Message):
    await message.answer(f"📌Заочное образование – форма организации учебного процесса, в которой сочетаются очное "
                         f"обучение и самообучение. При этом на самостоятельное изучение материала отводится 90 % "
                         f"времени.\n📌Учебный план, объем знаний, которые требуются от студента Института заочного "
                         f"образования, ничем не отличаются от плана и объемов очной формы обучения. Студенты "
                         f"Института заочного образования получают такой же диплом, как и студенты – очники."
                         f"\nЧто хотите о нём узнать?", reply_markup=info_institute_zo)
    await SearchInst.Q5.set()


@dp.message_handler(Text("Направления бакалавриата"), state=SearchInst.Q5)
async def direction_bk_zo(message: Message):
    await message.answer(f"Список направлений бакалавриата:\n"
                         f"1) 09.03.01 Информатика и вычислительная техника\n"
                         f"2) 09.03.02 Информационные системы и технологии\n"
                         f"3) 11.03.01 Радиотехника\n"
                         f"4) 11.03.02 Инфокоммуникационные технологии и системы связи\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes"
                         f"/idistance/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Направления магистратуры"), state=SearchInst.Q5)
async def direction_mg_zo(message: Message):
    await message.answer(f"Список направлений магистратуры:\n"
                         f"1) 09.04.01 Информатика и вычислительная техника\n"
                         f"2) 11.04.01 Радиотехника\n"
                         f"3) 11.04.02 Инфокоммуникационные технологии и системы связи\n"
                         f"Более подробно о направлениях можно узнать по ссылке:https://sibsutis.ru/institutes"
                         f"/idistance/"
                         , disable_web_page_preview=True)


@dp.message_handler(Text("Контакты"), state=SearchInst.Q5)
async def contacts_zo(message: Message):
    await message.answer(
        f"📌Адрес: ул. Гурьевская, 51, ауд. 603, 605а, 611\n"
        f"📌E-mail: dekanatzo@sibsutis.ru\n"
        f"📌И.о. директора Института заочного образования: Константин Владимирович Ломакин, телефон (383) 269-82-06;"
        f" E-mail: k.lomakin@sibguti.ru\n"
        f"📌·И.о. зам. Директора Института заочного образования: Анна Сергеевна Белезекова, телефон (383) 269-83-81,"
        f" E-mail: anna-belezekova@mail.ru\n"
        f"📌Специалисты по работе со студентами:\n"
        f"📌Мацкевич Марина Валерьевна, телефон (383) 269-82-56, E-mail: masha@sibsutis.ru\n"
        f"📌Смолянский Александр Леонтьевич, телефон (383) 269-82-83, E-mail: sal@sibsutis.ru\n"
        f"📌Приёмная комиссия заочного отделения - (383) 269-82-29"
        , disable_web_page_preview=True)


@dp.message_handler(Text("Минимальные баллы ЕГЭ"), state=SearchInst.Q5)
async def scores_zo(message: Message):
    await message.answer(f"📌09.03.01 Информатика и вычислительная техника (информатика/физика + математика + "
                         f"русский язык):\n"
                         f"Бюджет - 216 баллов\nВнебюджет - 115 баллов\nОсобое право - 191 баллов\n"
                         f"📌11.03.02 Инфокоммуникационные технологии и системы связи (информатика/физика + математика + "
                         f"русский язык):\n"
                         f"Особое право - 123 баллов\n"
                         f"📌09.03.02 Информационные системы и технологии (информатика/физика + математика + "
                         f"русский язык):\n"
                         f"Внебюджет - 109 баллов\n"
                         f"📌11.03.01 Радиотехника (информатика/физика + математика + "
                         f"русский язык):\n"
                         f"Особое право - 118 баллов\n"
                         f"📌11.03.00 электроника, радиотехника и системы связи (информатика/физика + математика + "
                         f"русский язык):\n"
                         f"Бюджет - 135 баллов\nВнебюджет - 116 баллов")


# Вывод информации о дополнительных увлечениях
@dp.message_handler(Text("Дополнительные увлечения"))
async def info_hobby(message: Message):
    await message.answer("📍Выберите о чём хотите узнать:", reply_markup=add_hobby)
    await SearchHobby.Q1.set()


# Информация о студенческих отрядах
@dp.message_handler(Text("Студенческие отряды"), state=SearchHobby.Q1)
async def info_stud_squads(message: Message):
    photo_stud_squads = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\1.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_stud_squads, f"📌Российские студенческие отряды – "
                                                             f"масштабное общественное движение, объединяющее "
                         f"студентов из разных регионов. По официальным данным, в молодёжной общероссийской "
                         f"общественной организации «Российские студенческие отряды» состоят более 240 000 "
                         f"участников из 74 субъектов федерации. В 2019 году общественное движение праздновало "
                         f"шестидесятилетие.\n📌Студенческие отряды СибГУТИ принимают активное участие в жизни "
                         f"движения, в различных социальных инициативах: добровольческих акциях «Вахта памяти», "
                         f"«Чистый берег», «Снежный десант», донорских акциях, работают с детскими домами, помогают "
                         f"пожилым людям и ветеранам ВОВ и т.д. А кроме того, проявляют свои таланты в спортивных "
                         f"и творческих мероприятиях.\n📌Сейчас в СибГУТИ действуют 5 направлений "
                         f"студенческих отрядов.\n📌Более подробнее о студенческих отрядах можно узнать "
                         f"по ссылке: https://vk.com/shso_sibguti", reply_markup=stud_squads)

    await SearchHobby.Q2.set()


# Информация о Отрядах проводников
@dp.message_handler(Text("Отряды проводников"), state=SearchHobby.Q2)
async def conductor_squads(message: Message):
    photo_conductor_squads = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\meridian.jpg', 'rb')
    photo_conductor_squads2 = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\non-stop.jpg', 'rb')
    await message.answer(f"📌Отряды проводников летом работают на железной дороге, в поездах дальнего следования.\n"
                         f"📌Средняя зарплата за месяц работы в отряде проводников - 35000 рублей.\n"
                         f"📌В СибГУТИ 2 отряда проводников:")
    await bot.send_photo(message.chat.id, photo_conductor_squads, f"«Меридиан» https://vk.com/sopmeridian")
    await bot.send_photo(message.chat.id, photo_conductor_squads2, f"«НонСтоп» https://vk.com/sop_non_stop")


# Информация о Вожатских отрядах
@dp.message_handler(Text("Вожатские отряды"), state=SearchHobby.Q2)
async def counselor_squads(message: Message):
    photo_counselor_squads = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\eridan.jpg', 'rb')
    photo_counselor_squads2 = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\sianie.jpg', 'rb')
    await message.answer(f"📌Педагогические отряды в летний период работают в детских оздоровительных лагерях на "
                         f"территории Российской Федерации.\n"
                         f"📌Средняя зарплата за месяц работы в педагогическом отряде - 15000 рублей.\n"
                         f"📌В СибГУТИ 2 вожатских отряда:\n")
    await bot.send_photo(message.chat.id, photo_counselor_squads, f"«Эридан» https://vk.com/spo__eridan")
    await bot.send_photo(message.chat.id, photo_counselor_squads2, f"«Сияние» https://vk.com/nro_spo_siyanie")


# Информация о Строительных отрядах
@dp.message_handler(Text("Строительные отряды"), state=SearchHobby.Q2)
async def builder_squads(message: Message):
    photo_builder_squads = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\svayz.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_builder_squads, f"📌В СибГУТИ всего один "
                                                                f"Строительный отряд «Связь» им. А. И. "
                                                                f"Покрышкина https://vk.com/"
                         f"sso_svyaz – старейший в СибГУТИ. Студентов в летний период ждут "
                         f"на строительных объектах федерального значения.\n"
                         f"📌Средняя зарплата за месяц работы в строительном отряде - 35000 рублей.")


# Информация о Сервисных отрядах
@dp.message_handler(Text("Сервисные отряды"), state=SearchHobby.Q2)
async def service_squads(message: Message):
    photo_service_squads = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\lux.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_service_squads, f"📌В СибГУТИ всего один "
                                                                f"Сервисный отряд «Люкс» https://vk.com/sservo_lux\n"
                         f"📌Летом предоставляет студентам работу в сфере общественного питания: в качестве барменов,"
                         f" официантов и поваров.\n"
                         f"📌Средняя зарплата за месяц работы в сервисном отряде - 20000 рублей (зависит от "
                         f"вида работы).")


# Информация о Сельскохозяйственных отрядах
@dp.message_handler(Text("Сельскохозяйственные отряды"), state=SearchHobby.Q2)
async def agriculture_squads(message: Message):
    photo_agriculture_squads = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\squads\\asstarta.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_agriculture_squads, f"📌в СибГУТИ всего "
                                                                    f"один Сельскохозяйственный "
                                                                    f"отряд «Астарта» https://vk.com/astarta.sibsutis\n"
                         f"📌Летом предоставляет студентам работу в разных тёплых городах России, в основном "
                         f"работая с растительностью, например, сбором яблок.")


# Информация о фестивалях
@dp.message_handler(Text("Фестивали"), state=SearchHobby.Q1)
async def info_festivals(message: Message):
    photo_festivals = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\festivals\\1.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_festivals,
                         f"📌Что он из себя представляет? − Фестиваль – это событие года!\n"
                         f"📌Каждый факультет заранее готовится, продумывает красивую и необычную программу, "
                         f"находит средства на костюмы, время на репетиции и силы на выступление. "
                         f"Затем наступает теплый месяц апрель, и команды выходят на сцену "
                         f"(каждая в назначенный день). Участники соревнуются в танцевальном, "
                         f"вокальном, актерском мастерствах, КВН-миниатюрах, прозе и в любых других "
                         f"жанрах. После подведения итогов самые лучшие номера всех факультетов можно "
                         f"ещё раз увидеть на гала-концерте фестиваля.\n📌Так происходит каждый год на протяжении "
                         f"уже практически 40 лет. За время существования этой славной традиции в СибГУТИ "
                         f"не было прецедентов, чтобы хотя бы один из шести факультетов отказался участвовать "
                         f"в «Студвесне». К ней начинают готовиться чуть ли не за год, идеи выступлений рождаются "
                         f"и копятся весь год, ожидая своего звёздного часа.\n📌Ссылка на паблик в "
                         f"Вконтакте: https://vk.com/club6040396", reply_markup=festivals)
    await SearchHobby.Q3.set()


# Информация о Фестивале ИВТ
@dp.message_handler(Text("Фестиваль ИВТ"), state=SearchHobby.Q3)
async def ivt_festival(message: Message):
    photo_ivt_festival = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\festivals\\ivt_festival.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_ivt_festival,
                         f"📌Если ты поступаешь на факультет ИВТ, и ты творческая личность, то переходи по "
                         f"ссылке и вступай в группу для подробной информации для участия в "
                         f"фестивале: https://vk.com/fest_ivt")


# Информация о Фестивале МРМ
@dp.message_handler(Text("Фестиваль МРМ"), state=SearchHobby.Q3)
async def mrm_festival(message: Message):
    photo_mrm_festival = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\festivals\\mrm_festival.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_mrm_festival,
                         f"📌Если ты поступаешь на факультет МРМ, и ты творческая личность, "
                         f"то переходи по ссылке и вступай в группу для "
                         f"подробной информации для участия в фестивале: https://vk.com/mpm_fest")


# Информация о Фестивале МТС
@dp.message_handler(Text("Фестиваль МТС"), state=SearchHobby.Q3)
async def mts_festival(message: Message):
    photo_mts_festival = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\festivals\\mts_festival.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_mts_festival,
                         f"📌Если ты поступаешь на факультет МТС, и ты творческая личность, "
                         f"то переходи по ссылке и вступай в группу для "
                         f"подробной информации для участия в фестивале: https://vk.com/fest_mts")


# Информация о Фестивале ГФ
@dp.message_handler(Text("Фестиваль ГФ"), state=SearchHobby.Q3)
async def gf_festival(message: Message):
    photo_gf_festival = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\festivals\\gf_festival.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_gf_festival,
                         f"📌Если ты поступаешь на факультет ГФ, и ты творческая личность, "
                         f"то переходи по ссылке и вступай в группу для "
                         f"подробной информации для участия в фестивале: https://vk.com/club1085454")


# Информация о Фестивале АЭС
@dp.message_handler(Text("Фестиваль АЭС"), state=SearchHobby.Q3)
async def aes_festival(message: Message):
    photo_aes_festival = open('D:\\учёба\\4 курс\\диплом\\My_Bot\\img\\festivals\\aes_festival.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo_aes_festival,
                         f"📌Если ты поступаешь на факультет АЭС, и ты творческая личность, "
                         f"то переходи по ссылке и вступай в группу для "
                         f"подробной информации для участия в фестивале: https://vk.com/festaes")


# Информация о профсоюзе студентов
@dp.message_handler(Text("Профсоюз студентов"), state=SearchHobby.Q1)
async def info_trade_union(message: Message):
    await message.answer(f"📌Профсоюзный комитет студентов СибГУТИ - это та организация, в которой каждый студент "
                         f"может реализовать свои идеи, получить помощь и консультации по разным аспектам "
                         f"студенческой жизни.", reply_markup=trade_union)
    await SearchHobby.Q4.set()


# Основная информация о профсоюзе студентов
@dp.message_handler(Text("Основное про профсоюз"), state=SearchHobby.Q4)
async def main_info_trade_union(message: Message):
    await message.answer(f"📌Если ты: \n1) Активный, умеешь писать статьи, фотографировать, снимать видео\n"
                         f"2) У тебя круто получается работать в команде или руководить ей\n"
                         f"3) У тебя множество идей, которые ты хочешь реализовать и заявить о себе\n"
                         f"4) Ты хочешь развиваться и всегда нацелен на помощь людям\n "
                         f"·В профкоме ты сможешь попробовать себя в:\n"
                         f"1) Пресс-центре - все направления SMM, работа с социальными сетями и новостными сайтами\n"
                         f"2) Event-направлении - организация всех самых крутых мероприятий в СибГУТИ\n"
                         f"3) Волонтерском движении, настольных играх, театральных и музыкальных направлениях, "
                         f"дизайне и многом другом!")


# Контакты профсоюза студентов
@dp.message_handler(Text("Социальные сети"), state=SearchHobby.Q4)
async def contacts_trade_union(message: Message):
    await message.answer(f"📌Страница в вконтакте:\nhttps://vk.com/profkom_sibsutis\n"
                         f"📌Страница в инстаграмме:https://www.instagram.com/profkom_sibsutis/"
                         f"", disable_web_page_preview=True)


# Информация о студклубе
@dp.message_handler(Text("Студклуб"), state=SearchHobby.Q1)
async def info_stud_club(message: Message):
    await message.answer(f"📌Неустанное внимание к творческой составляющей жизни студентов, их увлечениям и талантам – "
                         f"традиция НЭИС-СибГАТИ-СибГУТИ, бережно переносимая студенческим клубом из года в год на "
                         f"протяжении уже почти 45 лет.\n📌За десятилетия жизни клуба в его состав входили духовой "
                         f"и баянный оркестры, студия бальных и ансамбль народных танцев, в качестве художественных "
                         f"руководителей работали звёзды хорового искусства и хореографии. Коллективы и члены клуба "
                         f"удостоены многочисленных наград и званий российского и "
                         f"международного уровней.\n📌Более подробно о студенческом клубе можно узнать по ссылке:"
                         f"https://sibsutis.ru/students/studlife/studclub/", reply_markup=stud_club,
                         disable_web_page_preview=True)
    await SearchHobby.Q5.set()


# Информация о Народном коллективе академический хор им. В. Серебровского
@dp.message_handler(Text("Народный коллектив академический хор им. В. Серебровского"), state=SearchHobby.Q5)
async def chorus(message: Message):
    await message.answer(f"📌Академический хор был основан в 1973 году согласно постановлению ВЦСПС в целях "
                         f"эстетического воспитания и развития творчества студентов при студенческом клубе "
                         f"института связи. Основателем хора стал доцент Новосибирской государственной консерватории "
                         f"им. М. И. Глинки лауреат VII Всемирного фестиваля молодёжи и студентов в Вене Вадим "
                         f"Борисович Серебровский. В 1978 году академический хор получил звание «народного "
                         f"коллектива».\n📌На протяжении этих лет академический хор принимает активное участие в "
                         f"жизни города: концертные выступления, конкурсы, фестивали, гастрольные поездки в Томск, "
                         f"Красноярск, Иркутск, Одессу, Минск, Санкт-Петербург, Самару, Екатеринбург, Воронеж, "
                         f"Ташкент, Абакан и другие города.\n📌Более подробно о хоре можно узнать по ссылке: "
                         f"https://sibsutis.ru/students/studlife/studclub/akademicheskiy-khor-im-v-serebrovskogo."
                         f"php?clear_cache=Y", disable_web_page_preview=True)


# Информация о Народном коллективе стиль-балет «Единое дыхание»
@dp.message_handler(Text("Народный коллектив стиль-балет «Единое дыхание»"), state=SearchHobby.Q5)
async def one_breath(message: Message):
    await message.answer(f"📌В 1995 году на базе студенческого клуба Сибирского государственного университета "
                         f"телекоммуникаций и информатики был создан танцевальный коллектив стиль-балет "
                         f"«Единое дыхание», который сразу завоевал любовь студентов и преподавателей СибГУТИ.\n"
                         f"📌Первым руководителем коллектива была балетмейстер Татьяна Александровна Литвинова.\n"
                         f"📌Активно участвуя в творческой жизни, коллектив получил известность не только в вузе, "
                         f"но и Новосибирске и Новосибирской области. Стиль-балет «Единое дыхание» регулярно "
                         f"участвует в городских мероприятиях, посвящённых различным праздникам (День Города, "
                         f"Дельфийские игры, День Победы, юбилеи района и др.).\n📌Более подробно о народном коллективе "
                         f"можно узнать по ссылке: https://sibsutis.ru/students/studlife/studclub/edinoe-dykhanie."
                         f"php?clear_cache=Y", disable_web_page_preview=True)


# Информация о Вокальном джаз-ансамбле «Волярэ»
@dp.message_handler(Text("Вокальный джаз-ансамбль «Волярэ»"), state=SearchHobby.Q5)
async def volyare(message: Message):
    await message.answer(f"📌В 1984 году Наталья Ивановна Ягодина создала студенческий джаз-ансамбль «Волярэ» – "
                         f"старейший из существующих вокальных ансамблей студенческого клуба. Это первый коллектив,"
                         f" принесший СибГУТИ звание «лауреата» на «Российской студенческой весне» в Санкт-Петербурге"
                         f"(1999 г.)\n📌Ансамбль «Волярэ» является неоднократным лауреатом таких фестивалей и "
                         f"конкурсов, как «Российская студенческая весна» (г. Самара, 1998 г.), Международный "
                         f"фестиваль юмора и эстрадного искусства «Москва–Ялта–Транзит» (2007–2008 гг.), "
                         f"Международный молодёжный фестиваль Info accia (2008 г., г. Римини, "
                         f"Италия).\n📌Более подробно о вокальном джаз-ансамбле можно узнать по ссылке: "
                         f"https://sibsutis.ru/students/studlife/studclub/volyare.php?clear_cache=Y",
                         disable_web_page_preview=True)


# Информация о Мужском вокальном ансамбле «Септима»
@dp.message_handler(Text("Мужской вокальный ансамбль «Септима»"), state=SearchHobby.Q5)
async def septima(message: Message):
    await message.answer(f"📌В 2007 году на базе народного коллектива академического хора студентов "
                         f"СибГУТИ им. В. Серебровского (руководитель Ягодина Н. И.) был создан мужской "
                         f"вокальный ансамбль «Септима», который сразу стал популярным среди "
                         f"студентов и преподавателей вуза.\n📌Более подробно о вокальном ансамбле можно "
                         f"узнать по ссылке: https://sibsutis.ru/students/studlife/studclub/muzhskoy-"
                         f"vokalnyy-ansambl-septima.php?clear_cache=Y", disable_web_page_preview=True)


# Информация о Женском вокальном ансамбле «Синкопа»
@dp.message_handler(Text("Женский вокальный ансамбль «Синкопа»"), state=SearchHobby.Q5)
async def syncopation(message: Message):
    await message.answer(f"📌Женский вокальный ансамбль «Синкопа» зародился в 1998 году. Считается самым "
                         f"изысканным и нежным ансамблем, потому что это полностью женский вокальный состав. "
                         f"Регулярные занятия и репетиции всегда давали отличные результаты! За всё время "
                         f"существования коллектива девушки взяли много наград, дипломов и грамот.\n📌Более "
                         f"подробно о вокальном ансамбле можно узнать по ссылке: https://sibsutis.ru/students"
                         f"/studlife/studclub/sinkopa.php", disable_web_page_preview=True)


# Вывод информации о общежитиях
@dp.message_handler(Text("Общежития"))
async def info_dormitories(message: Message):
    await message.answer("    📌В процессе обучения заявления на предоставление места в общежитии "
                         "студентами очной и заочной формы обучения и магистрантами подаются в "
                         "соответствующие деканаты, аспирантами – в отдел аспирантуры. Оформление "
                         "документов осуществляется начальником отдела по работе с общежитиями по "
                         "направлению деканата или отдела аспирантуры.\n📌Все общежития находятся в 5-10 минутах "
                         "ходьбы от СибГУТИ\n    📌Более подробную информацию "
                         "о заселении в общежитие можно узнать по ссылке:\n"
                         "https://sibsutis.ru/abitur/obshchezhitiya/\n"
                         "    📌Выберите общежитие, о котором хотите узнать:\n", reply_markup=dormitories,
                         disable_web_page_preview=True)
    await SearchDormitory.Q1.set()


# Вывод информации о 1 общежитие
@dp.message_handler(Text("1 общежитие"), state=SearchDormitory.Q1)
async def first_dormitory(message: Message):
    await message.answer("  📌Предоставляются два этажа общежития № 1 по адресу ул. Нижегородская, "
                         "23 (для магистрантов и аспирантов СибГУТИ)\n  📌Общежитие коридорное. Стоимость:\n  773 "
                         "руб/месяц для студентов (за 6 кв. м.)\n  129 руб/месяц для аспирантов (за 1 кв. м.)\n"
                         "📌Контакты:\n  📌Зав. общежитием Валентина Владимировна Суворова, контактный телефон "
                         "(383) 269-82-17\n  📌Коменданты общежития:\n  Лейман Алекс Константинович и "
                         "Жамьянов Игорь Юрьевич, контактный телефон (383) 269-83-40")


# Вывод информации о 2 общежитие
@dp.message_handler(Text("2 общежитие"), state=SearchDormitory.Q1)
async def second_dormitory(message: Message):
    await message.answer("  📌Предоставляются пятиэтажное общежитие № 2 по адресу ул. Восход, 9\n  "
                         "📌Общежитие коридорное. Стоимость:\n  773 "
                         "руб/месяц для студентов (за 6 кв. м.)\n  129 руб/месяц для аспирантов (за 1 кв. м.)\n"
                         "📌Контакты:\n 📌Зав. общежитием Татьяна Васильевна Воеводина, контактный телефон (383) 266-92-"
                         "77")


# Вывод информации о 3 общежитие
@dp.message_handler(Text("3 общежитие"), state=SearchDormitory.Q1)
async def third_dormitory(message: Message):
    await message.answer("  📌Предоставляются девятиэтажное общежитие № 3 по адресу ул. Б.Богаткова, 63\n  "
                         "📌Общежитие секционное. Стоимость:\n  785 "
                         "руб/месяц для студентов (за 6 кв. м.)\n  131 руб/месяц для аспирантов (за 1 кв. м.)\n"
                         "📌Контакты:\n  📌Зав. общежитием Евгения Геннадьевна Севостьянова , контактный телефон "
                         "(383) 266-82-24")


# Вывод информации о 4 общежитие
@dp.message_handler(Text("4 общежитие"), state=SearchDormitory.Q1)
async def fourth_dormitory(message: Message):
    await message.answer("  📌Предоставляются девятиэтажное общежитие № 4 по адресу ул. Б.Богаткова, 63/1\n  "
                         "📌Общежитие секционное. Стоимость:\n  785 "
                         "руб/месяц для студентов (за 6 кв. м.)\n  131 руб/месяц для аспирантов (за 1 кв. м.)\n"
                         "📌Контакты:\n 📌Зав. общежитием Надежда Николаевна Осина,контактный телефон  (383) 266-51-14")

