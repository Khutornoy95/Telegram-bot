from telebot import types
from telebot.types import InlineKeyboardMarkup

def city_markup(cities) -> InlineKeyboardMarkup:
    keyboard_cities = types.InlineKeyboardMarkup()
    for key, value in cities.items():
        keyboard_cities.add(types.InlineKeyboardButton(text=value, callback_data=str(key)))
    return keyboard_cities


