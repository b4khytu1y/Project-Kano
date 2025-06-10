import asyncio
from datetime import datetime, time

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import router
from utils import get_user_tasks, get_all_users

import os

BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')


async def send_morning_message(bot: Bot):
    for user_id in get_all_users():
        tasks = get_user_tasks(user_id)
        text = 'Доброе утро! Желаю тебе продуктивного дня \U0001F4AA'
        if tasks:
            task_list = '\n'.join(f'- {t}' for t in tasks)
            text += f'\nВот список дел на сегодня:\n{task_list}'
        await bot.send_message(chat_id=user_id, text=text)


async def send_night_message(bot: Bot):
    for user_id in get_all_users():
        text = 'Спокойной ночи \U0001F319 Ты сегодня молодец. Горжусь тобой!'
        await bot.send_message(chat_id=user_id, text=text)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_morning_message, 'cron', hour=8, minute=0, args=(bot,))
    scheduler.add_job(send_night_message, 'cron', hour=22, minute=0, args=(bot,))
    return scheduler


async def main() -> None:
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = setup_scheduler(bot)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
