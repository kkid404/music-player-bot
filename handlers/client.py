from aiogram import types
from create_bot import dp, bot
from keyboards import start_keyboard, player_keyboard
from data_base.sqlite_db import CallDb
from models.User import User
from aiogram.types.input_media import InputMediaAudio, InputMediaPhoto, InputMediaVideo



#Ответ на комманду /start и /help
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    user = User(message)
    db = CallDb()
    await bot.send_message(message.from_user.id, "Приветственный текст!", reply_markup=start_keyboard)
    db.clean_count(user.telegram_id)
    if user.telegram_id not in db.read_all_user()[0]:
        user.add_user_database()

#Ответ на кнопку "Заяц"
@dp.message_handler(text = "ЗАЯЦ")
async def zayac(message: types.Message):
    user = User(message)
    db = CallDb()
    tracks = db.read_all_rap()[0]
    media = db.read_all_rap()[1]
    db.update_playlist("zayc", user.telegram_id)
    x = db.read_count(user.telegram_id)[0]
    try:
        await bot.send_audio(message.chat.id, tracks[x], reply_markup=player_keyboard())
        try:
            await bot.send_photo(message.chat.id, media[x])
        except:
            await bot.send_video(message.chat.id, media[x])
    except IndexError:
        await bot.send_message(message.chat.id, "Треки еще не добавлены", reply_markup=start_keyboard)

#Ответ на кнопку "Волк"
@dp.message_handler(text = "ВОЛК")
async def volk(message: types.Message):
    user = User(message)
    db = CallDb()
    tracks = db.read_all_rap()[0]
    tracks.reverse()
    media = db.read_all_rap()[1]
    media.reverse()
    db.update_playlist("volk", user.telegram_id)
    x = db.read_count(user.telegram_id)[0]
    try:
        await bot.send_audio(message.chat.id, tracks[x], reply_markup=player_keyboard())
        try:
            await bot.send_photo(message.chat.id, media[x])
        except:
            await bot.send_video(message.chat.id, media[x])
    except IndexError:
        await bot.send_message(message.chat.id, "Треки еще не добавлены", reply_markup=start_keyboard)

#Возврат к главному меню
@dp.message_handler(text = "Назад", state=None)
async def back(message: types.Message):
    await bot.send_message(message.from_user.id, "Хорошо", reply_markup=start_keyboard)

# Переключение трека вперед
@dp.callback_query_handler(text=["next"])
async def next_song(callback_query: types.CallbackQuery):
    user = User(callback_query)
    db = CallDb()
    next_msg_id = callback_query.message.message_id + 1
    playlist = db.read_all_user()[3]
    x = db.read_count(user.telegram_id)[0]
    x += 1
    print(x)
    db.update_count(x, user.telegram_id)  
    if playlist == 'zayc': 
        tracks = db.read_all_rap()[0]
        m = db.read_all_rap()[1]
    else:
        tracks = db.read_all_rap()[0]
        m = db.read_all_rap()[1]
        tracks.reverse()
        m.reverse()
    try:
        await callback_query.message.edit_media(media=InputMediaAudio(tracks[x]), reply_markup=player_keyboard())
        try:  
            await bot.edit_message_media(media=InputMediaPhoto(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)        
        except:
            await bot.edit_message_media(media=InputMediaVideo(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)
    except:
        x = 0
        db.update_count(x, user.telegram_id)  
        await callback_query.message.edit_media(media=InputMediaAudio(tracks[x]), reply_markup=player_keyboard())
        try:  
            await bot.edit_message_media(media=InputMediaPhoto(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)        
        except:
            await bot.edit_message_media(media=InputMediaVideo(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)


# Переключение трека назад
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("back"))
async def back_song(callback_query: types.CallbackQuery):
    user = User(callback_query)
    db = CallDb()
    message = types.Message
    next_msg_id = callback_query.message.message_id + 1
    playlist = db.read_all_user()[3]
    x = db.read_count(user.telegram_id)[0]
    x -= 1
    print(x)
    db.update_count(x, user.telegram_id)  
    if playlist == 'zayc': 
        tracks = db.read_all_rap()[0]
        m = db.read_all_rap()[1]
    else:
        tracks = db.read_all_rap()[0]
        m = db.read_all_rap()[1]
        tracks.reverse()
        m.reverse()
    try:
        await callback_query.message.edit_media(media=InputMediaAudio(tracks[x]), reply_markup=player_keyboard())
        try:  
            await bot.edit_message_media(media=InputMediaPhoto(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)        
        except:
            await bot.edit_message_media(media=InputMediaVideo(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)
    except:
        x = 0
        db.update_count(x, user.telegram_id)  
        await callback_query.message.edit_media(media=InputMediaAudio(tracks[x]), reply_markup=player_keyboard())
        try:  
            await bot.edit_message_media(media=InputMediaPhoto(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)        
        except:
            await bot.edit_message_media(media=InputMediaVideo(m[x]), chat_id=callback_query.from_user.id, message_id=next_msg_id)
        

#Выход из плеера
@dp.callback_query_handler(text=("leave"))
async def leave(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Хорошо', reply_markup=start_keyboard)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id + 1)