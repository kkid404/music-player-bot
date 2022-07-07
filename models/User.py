import sqlite3 as sq
from aiogram import types

from filters.all_filters import ADMIN


global base, cur
base = sq.connect('data.db') #подключаемся к бд, если её нет: создает
cur = base.cursor()

class User():
    def __init__(self, message: types.Message):
        self.telegram_id = message.from_user.id
        self.name = message.from_user.first_name
        self.trackcount = 0
        self.playlist = None

    def add_user_database(self):
        cur.execute("INSERT INTO user VALUES(?, ?, ?, ?)", (self.telegram_id , self.name, self.trackcount, self.playlist))
        base.commit()
