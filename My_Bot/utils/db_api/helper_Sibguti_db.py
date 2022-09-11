import sqlite3 as sq
from loader import bot


def sql_start():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    cur.execute("""CREATE TABLE if not exists teachers_list(fio text, phone_number text, email text, department text, 
    link text)""")
    base.commit()


def sql_add_many(x):
    cur.executemany("""INSERT INTO teachers_list VALUES(?, ?, ?, ?, ?)""", x)
    base.commit()


async def sql_add(state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO teachers_list VALUES(?, ?, ?, ?, ?)""", tuple(data.values()))
        base.commit()


async def sql_search(message):
    mess = message.text
    res = cur.execute("""SELECT * FROM teachers_list WHERE fio = ? """, [mess]).fetchone()
    if res is None:
        await bot.send_message(message.from_user.id, text=f"Такого преподавателя нет или вы ввели неверные данные.\n"
                                                          f"Нажмите снова на поиск по фио и повторите попытку.")
    else:
        await bot.send_message(message.from_user.id, text=
        f"📍Фио: {res[0]}\n"
        f"📍Телефон: {res[1]}\n"
        f"📍Почта: {res[2]}\n"
        f"📍Место работы: {res[3]}\n"
        f"📍Ссылка на профиль: {res[-1]}", disable_web_page_preview=True)


async def sql_search_lastname(message):
    mess = message.text + "%"
    res = cur.execute("""SELECT * FROM teachers_list WHERE fio LIKE ? """, [mess, ]).fetchall()
    if res is None:
        await bot.send_message(message.from_user.id, text=f"С такой фамилией преподаватели не были найдены "
                                                          f"или вы ввели неверно фамилию.\nНажмите снова на поиск по "
                                                          f"фамилии и повторите попытку.")
    else:
        for x in res:
            await bot.send_message(message.from_user.id, text=
            f"📍Фио: {x[0]}\n"
            f"📍Телефон: {x[1]}\n"
            f"📍Почта: {x[2]}\n"
            f"📍Место работы: {x[3]}\n"
            f"📍Ссылка на профиль: {x[-1]}\n", disable_web_page_preview=True)
