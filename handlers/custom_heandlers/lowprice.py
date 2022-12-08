from telebot.types import Message
from states.personal_information import UserInfoState
from loader import bot
from utils.find_destination_id import destination_id
from keyboards.inline.cities_buttons import city_markup
from keyboards.inline.calendar import run_calendar, get_date

@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    bot.reply_to(message, 'Введите город (поиск по городам России на данный момент временно не работает)')

@bot.message_handler(state=UserInfoState.input_city)
def find_city(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
    possible_options = destination_id(data['input_city'])

    bot.reply_to(message, 'Уточните, пожалуйста:', reply_markup=city_markup(possible_options))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call) -> None:
    if call.message:
        bot.set_state(call.message.from_user.id, UserInfoState.user_select_id, call.message.chat.id)
        with bot.retrieve_data(call.message.from_user.id, call.message.chat.id)as data:
            data['destination_id'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        run_calendar(call.message)



        find_hotels(call, call.data)

def find_hotels(message, destination_id):
    pass