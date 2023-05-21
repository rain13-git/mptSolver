from aiogram.dispatcher import FSMContext

from mptSolver.bot import dp, bot
from mptSolver.config import Config
from aiogram.types import LabeledPrice, ContentType, invoice
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from yoomoney import Quickpay, Client
import random

from mptSolver.services import DataBase
from mptSolver.markups import subjectsInline, subjects_menu, admin_actions, admin_file, check
from mptSolver.services import help_exit
from mptSolver.states import Subject

db = DataBase('exerDB.sql')


async def send(message: Message, state: FSMContext):
    # сохраняй file_unique_id а отправляй по file_id
    # print(file_id)  # этот идентификатор нужно где-то сохранить
    admin = await db.getAdmin()
    user_id = message.from_id
    if message.document:
        file_uniq = message.document.file_unique_id
        await db.insertFile(user_id, file_uniq)
        file_id = message.document.file_id
        await bot.send_document(admin[-1][0], file_id, reply_markup=admin_actions)
    if message.photo:
        file_uniq = message.photo[-1].file_unique_id
        await db.insertPhoto(user_id, file_uniq)
        file_id = message.photo[-1].file_id
        await bot.send_photo(admin[-1][0], file_id, reply_markup=admin_actions)


@dp.message_handler()
async def message_hand(message: Message, state: FSMContext):
    await help_exit(message, state)
    await db.closeState(message.chat.id, '1')


@dp.message_handler(state=Subject.file, content_types=['text', 'document', 'photo'])
async def say_ref(message: Message, state: FSMContext):
    user_id = message.from_id
    try:
        if message.text == 'Меню':
            raise Exception('err')
        await send(message, state)
        await message.answer('Ждем оценки Вашего задания (в среднем до 30м)')
    except Exception:
        await message_hand(message, state)
    finally:
        await state.reset_state()
        # await db.closeState(user_id, '1')


@dp.callback_query_handler(lambda call: call.data.find('user') == 0)
async def user_answer(call: CallbackQuery):
    if call.data[-1] == '0':
        price = await db.getAmount(call.message.chat.id)
        comment = f'{str(call.message.chat.id)}_{str(random.randint(1000, 9999))}'
        price = await db.getAmount(call.message.chat.id)
        price = price[-1][0]
        quickpay = Quickpay(
            receiver='4100118200745354',
            quickpay_form='shop',
            targets='payment solution',
            paymentType='SB',
            sum=price,
            label=comment
        )
        print(comment)
        await call.message.answer(f'Стоимость заказа {price}Р', reply_markup=check(quickpay.redirected_url, comment))
        # prices = [LabeledPrice(label='задание', amount=price[-1][0]*100)]
        # await pay(call.from_user['id'], Config.pay_token, prices)
    else:
        await call.message.answer('В следующий раз!', reply_markup=subjectsInline)


@dp.callback_query_handler(lambda call: call.data.find('check') == 0)
async def check_pay(call: CallbackQuery):
    admin = await db.getAdmin()
    p2p = await db.getP2P()
    label = call.data[6:]
    paid_state = await db.checkPaidState(call.message.chat.id)
    paid_state = paid_state[-1][0]
    if paid_state == 0:
        client = Client(p2p[-1][0])
        history = client.operation_history(label=label)
        try:
            operation = history.operations[-1]
            if operation.status == 'success':
                await db.paidState(call.message.chat.id, '1')
                await call.message.answer(Config.wait)
                await bot.send_message(admin[-1][0], Config.wait, reply_markup=admin_file)
        except Exception as e:
            await call.message.answer(Config.wait_pay)
    else:
        # await db.paidState(call.message.chat.id, '1')
        await call.message.answer(Config.wait)
        await bot.send_message(admin[-1][0], Config.wait, reply_markup=admin_file)


@dp.callback_query_handler(lambda call: call.data.find('grade') == 0)
async def call_grade(call: CallbackQuery):
    await db.setGrade(Config.user, call.data[-1])
    await db.closeState(Config.user, '1')
    await call.message.answer('Спасибо за оценку! Ждем Вас снова', reply_markup=subjectsInline)


# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_check(check: PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(check.id, ok=True)
#
#
# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def success(message: Message):
#     await db.paidState(message.from_id, '1')
#     await message.answer(Config.wait)
#     await bot.send_message(Config.admin, Config.wait, reply_markup=admin_file)



