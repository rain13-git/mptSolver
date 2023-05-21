from aiogram.dispatcher import FSMContext

from mptSolver.bot import dp, bot
from mptSolver.config import Config
from aiogram.types import LabeledPrice, ContentType
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ShippingQuery, ShippingOption, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text

from mptSolver.handlers.subject import message_hand
from mptSolver.services import DataBase
from mptSolver.markups import subjectsInline, subjects_menu, admin_actions, user_actions, grades
from mptSolver.services import help_exit
from mptSolver.states import Subject, Admin


db = DataBase('exerDB.sql')


async def send(call, user_id):
    if call.data == 'action-1':
        call.message.text = 'Извините, но мы не сможем выполнить Ваше задание'
        call.message.reply_markup = subjectsInline
        await call.message.send_copy(user_id)
    else:
        await Admin.price.set()
        await call.message.answer('Оцени бро)')


@dp.callback_query_handler(lambda call: call.data.find('action') == 0)
async def call_hand(call: CallbackQuery):
    if call.message.photo:
        file_id = call.message.photo[-1].file_id
        file_uniq = call.message.photo[-1].file_unique_id
        user_id = await db.getUserByPhoto(file_uniq)
        Config.user = user_id
        await send(call, user_id)
    # сохраняй file_unique_id а отправляй по file_id
    if call.message.document:
        file_uniq = call.message.document.file_unique_id
        file_id = call.message.document.file_id
        user_id = await db.getUserByPhoto(file_uniq)
        await send(call, user_id)


@dp.callback_query_handler(lambda call: call.data.find('send') == 0)
async def call_file(call: CallbackQuery):
    await call.message.answer('ТЫ ГЕНИЙ!')
    await Admin.solve.set()


@dp.message_handler(state=Admin.price)
async def evaluate(message: Message, state: FSMContext):
    await db.setAmount(Config.user, int(message.text))
    message.text += 'Р будет стоить выполение Вашей задачи'
    message.reply_markup = user_actions
    await message.send_copy(Config.user)
    await state.reset_state()


@dp.message_handler(state=Admin.solve, content_types=['text', 'document', 'photo'])
async def send_file(message: Message, state: FSMContext):
    if message.text:
        await message.answer('Долбоеб файл отправь)))')
    if message.document:
        file_id = message.document.file_id
        await bot.send_document(Config.user, file_id)
    if message.photo:
        file_id = message.photo[-1].file_id
        await bot.send_photo(Config.user, file_id)
    await bot.send_message(Config.user, 'Оцените пожалуйста!', reply_markup=grades)
    await state.reset_state()
