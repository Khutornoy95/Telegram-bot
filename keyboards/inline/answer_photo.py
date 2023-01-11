from telebot import types
from telebot.types import InlineKeyboardMarkup

def photo_markup() -> InlineKeyboardMarkup:
    keyboard_photo = types.InlineKeyboardMarkup()
    keyboard_photo.add(types.InlineKeyboardButton(text='Да', callback_data='Да'))
    keyboard_photo.add(types.InlineKeyboardButton(text='Нет', callback_data='Нет'))
    return keyboard_photo
