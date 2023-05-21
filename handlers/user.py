from aiogram.dispatcher import FSMContext

from mptSolver.bot import dp
from mptSolver.config import Config
from aiogram.types import LabeledPrice, ContentType
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ShippingQuery, ShippingOption, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from mptSolver.services import DataBase
from mptSolver.markups import subjectsInline, subjects_menu
from mptSolver.states import Subject


db = DataBase('exerDB.sql')


@dp.message_handler(Command('start'))
async def start(message: Message):
    try:
        await db.createUser(message.from_id, message.from_user.full_name)
    except Exception as e:
        pass
    finally:
        await message.answer(Config.sayHi, reply_markup=subjectsInline)
        await message.answer(Config.reference, reply_markup=subjects_menu)


@dp.callback_query_handler(lambda call: call.data.find('subject') == 0)
async def subjects(call: CallbackQuery):
    print(call.data)
    for subject in Config.subjectsData:
        if call.data == f'subject_{subject}':
            await call.message.answer(Config.subjectsData[subject] + '\n' + Config.gen_reference)
            if call.data != 'subject_Литература':
                await call.message.answer(Config.time_ref)
            await call.message.answer(Config.send)
            await db.createOrder(call.message.chat.id, call.data[8:])
            await Subject.file.set()



