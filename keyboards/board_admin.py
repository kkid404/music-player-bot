from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base.sqlite_db import CallDb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


#основная админская клавиатура
upload = KeyboardButton("Загрузить трек")
tracks = KeyboardButton("Загруженные треки")
send_message = KeyboardButton("Отправить сообщение")
back = KeyboardButton("Назад")
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.row(upload, send_message, tracks, back)


#клавиатура отмены загрузки трека
cancel = KeyboardButton("Назад")
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(cancel)

#клавиатура с загруженными треками
def track_keyboard():
    db = CallDb()
    names = db.read_all_rap()[2]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in names:
        track = KeyboardButton(name)
        keyboard.row(track)
    keyboard.row(cancel)
    return keyboard

#Клавиатура для удаления трека
def delete_keyboard(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    delete = InlineKeyboardButton(text="Удалить", callback_data=f"del_{message}")
    keyboard.add(delete)
    return keyboard

#Клавиатура для рассылки
send_kb = InlineKeyboardMarkup(row_width=2)
send = InlineKeyboardButton(text="Отправить", callback_data='send')
no_send = InlineKeyboardButton(text="Не отправлять", callback_data='no_send')
send_kb.add(send, no_send)
