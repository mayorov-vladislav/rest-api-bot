import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from handlers.admin_private import admin_private_router
from common.bot_cmd_list import *
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# TOKEN = 'TOKEN_BOT'
# bot = Bot(token=TOKEN)

bot = Bot(token=os.getenv("TOKEN"), parse_mode=ParseMode.HTML)
bot.my_admin_list = []

storage = MemoryStorage()
dp = Dispatcher(fsm_strategy=FSMStrategy.GLOBAL_USER, storage=storage)

dp.include_routers(
    user_private_router,
    admin_private_router,
    user_group_router,
)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=private_user_cmd, scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await asyncio.sleep(2)


print("Бот успешно запущен...")
asyncio.run(main())
