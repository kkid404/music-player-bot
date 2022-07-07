from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import configparser
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Читает токен бота из settings.ini
config = configparser.ConfigParser()
config.read("settings.ini")
TOKEN = config["BOT"]["TOKEN"]

# Обращение к оперативной памяти
storage = MemoryStorage()

# Основные переменные бота
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)



