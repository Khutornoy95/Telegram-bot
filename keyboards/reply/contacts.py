from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Отправить контакты', request_contact=True))
    return keyboard