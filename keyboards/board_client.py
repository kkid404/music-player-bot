from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


#Стартовая клавиатура
zayc = KeyboardButton('ЗАЯЦ')
volk = KeyboardButton('ВОЛК')
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_keyboard.add(zayc).add(volk)


#Клавиатура-плеер
def player_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    next = InlineKeyboardButton(text="Вперед", callback_data="next")
    backtrack = InlineKeyboardButton(text="Назад", callback_data="back")
    back = InlineKeyboardButton(text="Выйти", callback_data="leave")
    keyboard.add(backtrack, next).insert(back)
    return keyboard


