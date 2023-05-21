from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from mptSolver.bot import dp
from mptSolver.config import Config
from mptSolver.markups import subjectsInline, admin_actions
from mptSolver.services import DataBase

db = DataBase('exerDB.sql')

async def help_exit(message: Message, state: FSMContext):
    if message.text == 'Меню':
        await state.reset_state()
        status = await state.get_state()
        print(status)
        await message.answer(Config.sayHi, reply_markup=subjectsInline)
        return False

