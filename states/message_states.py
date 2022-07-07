from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageMessage(StatesGroup):
    message = State()