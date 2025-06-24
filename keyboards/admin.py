from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/list")],
            [KeyboardButton(text="Просмотр заявки"), KeyboardButton(text="Отметить просмотренной")],
            [KeyboardButton(text="Удалить заявку")],
        ],
        resize_keyboard=True
    ) 