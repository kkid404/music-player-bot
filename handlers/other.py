from create_bot import dp, bot
from aiogram import types
from data_base.sqlite_db import CallDb
from keyboards import delete_keyboard
from filters import ADMIN

# Посылает треки, если в сообщении содержится его название
@dp.message_handler()
async def song(message: types.Message):
    db = CallDb()
    tracks = db.read_all_rap()[0]
    names =  db.read_all_rap()[2]
    if message.from_user.id in ADMIN: # проверка на админа
        if message.text in names:
            count = names.index(message.text)
            await bot.send_audio(message.chat.id, tracks[count], reply_markup=delete_keyboard(message.text))
        else:
            pass
