from aiogram.dispatcher.filters.state import State, StatesGroup

#Класс для машины состояний, переменные - объекты, которые принимает машина состояний и записывает в базу данных
class StorageTrack(StatesGroup):
    track = State()
    media = State()
    name = State()