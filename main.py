from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
import handlers
from handlers.admin import ADMIN


async def on_start(event): #если оставлять функцию пустой, выкидывает ошибку
    print("Все работает")
    print(ADMIN)
    sqlite_db.sql_start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)