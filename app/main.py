import os, sys
sys.dont_write_bytecode = True

from dotenv import load_dotenv
load_dotenv()

from icecream import install
install()

from databases.models import async_create_db

import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from handlers.init_handlers import init_router
from handlers.menu_handlers import menu_router
from utils.commands import bot_cmds

async def main():
    TG_TOKEN = os.getenv('TG_TOKEN')

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(init_router)
    dp.include_router(menu_router)

    await async_create_db()
    # await bot.set_my_commands(commands=[], scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        pass



#TODO: изменить/уменьшить размер кнопки комманд или вообще убрать их и сделать reply kb