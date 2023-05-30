
from aiogram import Bot, Dispatcher
import asyncio, aiohttp
from setting import settings
from aiogram.fsm.storage.memory import MemoryStorage


storage = MemoryStorage()
global bot
bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")


async def start():
    global dp
    dp = Dispatcher(storage=storage)
    from handlers import blasphemyFilter, client_arm, admin_handler, admin_add, client_registration
    from utils import sq_lite_db_books, sq_lite_db_users

    await client_arm.register_client_handlers(dp)
    await client_registration.register_client_registration(dp)
    await admin_handler.register_admin_handlers(dp)
    await admin_add.register_admins(dp)
    await sq_lite_db_books.register_DB_handlers(dp)
    await blasphemyFilter.register_blasphemy_handlers(dp)
    
    try:
        await sq_lite_db_books.db_connect()
    except:
        print("BOOKS DATA BASE NOT CONNECTED")
    else:
        print("BOOKS DATA BASE CONNECTED")

    try:
        await sq_lite_db_users.db_connect_users()
    except:
        print("USERS DATA BASE NOT CONNECTED")
    else:
        print("USERS DATA BASE CONNECTED")
        

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, close_bot_session=True)
    finally:
        await bot.session.close()
        session = aiohttp.ClientSession()
        await session.close()

if __name__ == "__main__":
    asyncio.run(start())

