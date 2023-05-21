from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, KeyboardButton
from mptSolver.config import Config
from mptSolver.states import Subject

subjects_menu = ReplyKeyboardMarkup(resize_keyboard=True)
subjectsInline = InlineKeyboardMarkup(row_width=2)
admin_actions = InlineKeyboardMarkup(row_width=2)
user_actions = InlineKeyboardMarkup(row_width=2)
admin_file = InlineKeyboardMarkup().insert(InlineKeyboardButton(text='Отправить файл', callback_data='send'))
grades = InlineKeyboardMarkup(row_width=5)

for subject in Config.subjects:
    subjectsInline.insert(InlineKeyboardButton(text=subject, callback_data=f'subject_{subject[2:]}'))

for id, action in enumerate(Config.admin_actions):
    admin_actions.insert(InlineKeyboardButton(text=action, callback_data=f'action-{id}'))

for id, action in enumerate(Config.user_actions):
    print(f'user-{id}')
    user_actions.insert(InlineKeyboardButton(text=action, callback_data=f'user-{id}'))

for grade in Config.grade:
    grades.insert(InlineKeyboardButton(text=grade, callback_data=f'grade-{grade}'))


def check(url="", bill = ""):
    pay_menu = InlineKeyboardMarkup(row_width=2)
    btn_pay = InlineKeyboardButton(text=Config.pay_actions[0], url=url)
    pay_menu.insert(btn_pay)
    btn_check = InlineKeyboardButton(text=Config.pay_actions[1], callback_data=f'check_{bill}')
    pay_menu.insert(btn_check)
    return pay_menu

subjects_menu.add(KeyboardButton(text='Меню'))

