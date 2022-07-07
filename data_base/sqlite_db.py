from email import message
import sqlite3 as sq
from filters import ADMIN
from aiogram import types
from models.User import User

global base, cur
base = sq.connect('data.db') #подключаемся к бд, если её нет: создает
cur = base.cursor()

def sql_start():
    if base: # выводится при успешном подключении
        print("База данных успешно подключена!")
    base.execute('CREATE TABLE IF NOT EXISTS rap(tracks TEXT, media TEXT, names TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS user(telegram_id INTEGER PRIMARY KEY, name TEXT, count INTEGER, playlist TEXT)')
    base.commit()

# функция для записи песен в бд
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO rap VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

class CallDb():
    def __init__(self):
        self.cur = cur
        self.base = base

    # Читает всю таблицу с музыкой
    def read_all_rap(self):
        music = []
        media = []
        names = []
        for ret in self.cur.execute('SELECT * FROM rap').fetchall():
            music.append(ret[0])
            media.append(ret[1])
            names.append(ret[2])
        return music, media, names
        
    # Читает всю таблицу с пользователями
    def read_all_user(self):
        id = []
        names = []
        count = []
        playlist = ''
        for ret in self.cur.execute('SELECT * FROM user').fetchall():
            id.append(ret[0])
            names.append(ret[1])
            count.append(ret[2])
            playlist = ret[3]
        return id, names, count, playlist

    # Обновление счетчика
    def update_count(self, data, user):
        self.cur.execute(f'UPDATE user SET count = {data} WHERE telegram_id == {user}')
        self.base.commit()

    # Обнуление счетчика
    def clean_count(self, user):
        self.cur.execute(f'UPDATE user SET count = {0} WHERE telegram_id == {user}')
        self.base.commit()

    def read_count(self, user):
        for ret in self.cur.execute(f'SELECT count FROM user WHERE telegram_id == {user}').fetchall():
            return ret
              
    # Обновление плэйлиста
    def update_playlist(self, data, user):
        self.cur.execute('UPDATE user SET playlist = ? WHERE telegram_id == ?', (data, user))
        self.base.commit()

    #удаляет песню из базы по названию
    def sql_delete_command(self, data):
        self.cur.execute('DELETE FROM rap WHERE names == ?', (data,))
        self.base.commit()