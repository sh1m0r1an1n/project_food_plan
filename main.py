import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from Handlers.handlers import user_private_router
from Common.bot_cmds_list import private


async def main():
    load_dotenv()
    dp = Dispatcher()
    dp.include_routers(user_private_router)
    BOT_TOKEN = os.getenv('BOT_TG_TOKEN')
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
