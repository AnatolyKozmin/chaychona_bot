import asyncio
from aiogram import Bot, Dispatcher, types 

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


bot = Bot()
dp = Dispatcher()


async def main():
    print("Бот работает")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())