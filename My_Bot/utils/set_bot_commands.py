from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("menu", "Вызвать меню"),
            types.BotCommand("cancel", "Отменить текущее действие"),
            types.BotCommand("back", "Вернуться назад"),
        ]
    )
