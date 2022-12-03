from telebot.types import Message
from states.personal_information import UserInfoState
from loader import bot
from utils.find_destination_id import destination_id

@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    bot.reply_to(message, 'Введите город (поиск по городам России на данный момент временно не работает)')

@bot.message_handler(state=UserInfoState.input_city)
def find_city(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
    possible_options = destination_id(data['input_city'])