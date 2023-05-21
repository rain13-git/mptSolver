import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import filters, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from mptSolver.services import DataBase

logging.basicConfig(level=logging.INFO)

db = DataBase('exerDB.sql')
token = db.getToken()
bot = Bot(token=token[-1][0])
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    from handlers import dp
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('bot stopped')