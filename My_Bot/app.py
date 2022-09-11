from aiogram import executor
from loader import dp
from utils.db_api.helper_Sibguti_db import sql_start  # , sql_add_many, x
import middlewares, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Запускаем базу данных
    sql_start()
    # sql_add_many(x)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
