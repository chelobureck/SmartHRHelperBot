import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from utils.logger import setup_logger
from database.db import create_db
from handlers import user, admin

async def main():
    setup_logger()
    logging.info('Бот запускается...')
    await create_db()
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(user, admin)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 