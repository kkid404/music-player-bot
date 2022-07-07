from aiogram.dispatcher import FSMContext
from states.track_states import StorageTrack
from states.message_states import StorageMessage
from aiogram import types
from create_bot import dp, bot
from data_base.sqlite_db import sql_add_command, CallDb
from keyboards import admin_keyboard, start_keyboard, cancel_keyboard, track_keyboard, send_kb
from aiogram.dispatcher.filters import Text
from filters import ADMIN
import asyncio

 
# Ответ на команду админ
@dp.message_handler(commands=["admin"])
async def admin_start(message: types.Message):
    if str(message.from_user.id) in ADMIN: # проверка на админа
        await bot.send_message(message.from_user.id, "Леха здарова!", reply_markup=admin_keyboard)
    else:
        await bot.send_message(message.from_user.id, "Не понимаю о чем ты, используй команду /start", reply_markup=start_keyboard)

# Рассылка сообщений всем пользователям
@dp.message_handler(text="Отправить сообщение", state=None)
async def send_all_user(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:
        await message.reply("Напиши сообщение для рассылки:")
        await StorageMessage.message.set()
    else:
        await bot.send_message(message.from_user.id, "Не понимаю о чем ты, используй команду /start", reply_markup=start_keyboard)

#Принятие текста для рассылки
@dp.message_handler(state=StorageMessage.message)
async def input_text(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:
        db = CallDb()
        async with state.proxy() as data:
            data["message"] = str(message.text)
        users = db.read_all_user()[0]
        await StorageMessage.message.set()
        await bot.send_message(message.from_user.id, f'Ты собираешься отправить:\n{message.text}\n{len(users)} пользователям?', reply_markup=send_kb)


#Добавление треков
@dp.message_handler(text = "Загрузить трек", state=None)
async def cm_start(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:
        await StorageTrack.track.set() #Здесь Бот ожидает получить трек
        await message.reply("Отправь трек", reply_markup=cancel_keyboard)
    else:
        await bot.send_message(message.from_user.id, "Не понимаю о чем ты, используй команду /start", reply_markup=start_keyboard)


#Обработка кнопки "назад"
@dp.message_handler(text = "Назад", state=None)
async def back(message: types.Message):
    if str(message.from_user.id) in ADMIN:
        await bot.send_message(message.from_user.id, "Хорошо", reply_markup=start_keyboard)
    else: 
        await bot.send_message(message.from_user.id, "Не понимаю о чем ты, используй команду /start", reply_markup=start_keyboard)

#Получение трека
@dp.message_handler(content_types=['audio'], state=StorageTrack.track)
async def load_audio(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:
        async with state.proxy() as data:
            data['audio'] = message.audio.file_id
        await StorageTrack.next() #Здесь мы переходим к следующему шагу
        await message.reply("Теперь пришли любой файл к треку:")

#Получение названия тека и запрос медиа
@dp.message_handler(content_types=['photo', 'video'], state=StorageTrack.media)
async def load_media(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['media'] = message.photo[0].file_id
        except:
            data['media'] = message.video.file_id
        await StorageTrack.next()
        await message.reply("Теперь пришли название песни")

#Получение названия и завершение
@dp.message_handler(content_types=['text'], state=StorageTrack.name)
async def load_name(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMIN:
        async with state.proxy() as data:
            data['name'] = message.text
        await sql_add_command(state)
        await state.finish()
        await message.reply("Готово!", reply_markup=admin_keyboard)
    else:
        await bot.send_message(message.from_user.id, "Не понимаю о чем ты, используй команду /start", reply_markup=start_keyboard)

#Выход из машины состояния
@dp.message_handler(Text(equals='Назад', ignore_case=True), state="*")
async def cancel_handlers(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Хорошо!", reply_markup=start_keyboard)

# Просмотр загруженных в бота треков
@dp.message_handler(lambda message: message.text == "Загруженные треки", state=None)
async def admin_start(message: types.Message):
    if str(message.from_user.id) in ADMIN: # проверка на админа
        await bot.send_message(message.from_user.id, "Твои треки", reply_markup=track_keyboard())
    else:
        await bot.send_message(message.from_user.id, "Не понимаю о чем ты, используй команду /start", reply_markup=start_keyboard)

# Обработка удаления
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_'))
async def del_callback_run(callback_query: types.CallbackQuery):
    db = CallDb()
    await db.sql_delete_command(callback_query.data.replace("del_", ""))  
    await callback_query.answer(text=f'{callback_query.data.replace("del_", "")} удалена.')
    db.read_all_rap()[2]

# Обработка рассылки
@dp.callback_query_handler(text=["send", "no_send"], state=StorageMessage.message)
async def send_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    if callback_query.data == "no_send":
        await state.finish()
        await callback_query.message.answer("Рассылка отменена.")
    else:
        await callback_query.message.answer("Рассылка началась...")
        async with state.proxy() as data:
            send_ad_message = data["message"]
        await state.finish()
        asyncio.create_task(send_message_to_user(send_ad_message, callback_query.from_user.id))

# Отправка сообщений
async def send_message_to_user(message, id):
    receive_users, block_users = 0, 0
    db = CallDb()
    users = db.read_all_user()[0]
    for user in users:
        try:
            await bot.send_message(user, message)
            receive_users += 1
        except:
            block_users += 1
        await asyncio.sleep(0.5)
    await bot.send_message(id, f'Рассылка завершена!\nПользователей получило сообщение: {receive_users}\nПользователей не получило сообщение: {block_users}')
