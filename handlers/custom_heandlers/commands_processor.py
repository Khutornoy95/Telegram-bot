from telebot.types import Message, CallbackQuery
import json
from states.personal_information import UserInfoState
from loader import bot
from utils.requests import api_request
from utils.find_hotels import find_hotels
from utils.find_hotels_bestdeal import find_hotels_bestdeal
from keyboards.inline.cities_buttons import city_markup
from keyboards.inline.calendar import run_calendar
from keyboards.inline.answer_photo import photo_markup
from telegram_bot_calendar import DetailedTelegramCalendar
from keyboards.inline.calendar import LSTEP_RU
from datetime import date
from database.database import db, History

@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'lowprice'
    bot.reply_to(message, 'Введите город (поиск по городам России на данный момент временно не работает)')

@bot.message_handler(commands=['highprice'])
def highprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'highprice'
    bot.reply_to(message, 'Введите город (поиск по городам России на данный момент временно не работает)')

@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.input_city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'bestdeal'
    bot.reply_to(message, 'Введите город (поиск по городам России на данный момент временно не работает)')

@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    with db:
        history = History.select().where(History.chat_id == message.chat.id)
        for command in history:
            bot.send_message(message.chat.id, 'Команда: ' + command.command + '\nДата и время: '
                             + str(command.date) + '\nНайденные отели: ' + command.hotels[1: -2])

@bot.message_handler(state=UserInfoState.input_city)
def find_location(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['input_city'] = message.text
    response = api_request('locations/v3/search', {'q': data['input_city'], 'locale': 'ru_RU'}, 'GET')
    if response:
        data_api = json.loads(response)
        possible_options = {}
        for elem in data_api["sr"]:
            if elem['type'] == 'CITY' or elem['type'] == 'NEIGHBORHOOD':
                possible_options[elem['gaiaId']] = elem['regionNames']['fullName']
        if possible_options:
            bot.set_state(message.from_user.id, UserInfoState.buttons_city, message.chat.id)
            bot.reply_to(message, 'Уточните, пожалуйста:', reply_markup=city_markup(possible_options))
        else:
            bot.send_message(message.chat.id, 'По запросу ничего не нашлось, попробуйте ещё раз.')
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте ещё раз.')

@bot.message_handler(state=UserInfoState.buttons_city)
def find_city(message: Message) -> None:
    bot.reply_to(message, 'Пожалуйста, нажмите на кнопку.')

def filter_func(call) -> bool:
    state = bot.get_state(call.from_user.id, call.message.chat.id)
    return state is UserInfoState.buttons_city

@bot.callback_query_handler(func=filter_func)
def callback_query(call: CallbackQuery) -> None:
    if call.message:
        bot.set_state(call.from_user.id, UserInfoState.date_of_entry, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['destination_id'] = str(call.data)
        bot.send_message(call.message.chat.id, 'Введите дату заселения')
        run_calendar(call.from_user.id)

@bot.message_handler(state=UserInfoState.date_of_entry)
def entry_date(message: Message) -> None:
    bot.reply_to(message, 'Пожалуйста, нажмите на кнопку.')

def filter_func_entry_date(call: CallbackQuery) -> bool:
    state = bot.get_state(call.from_user.id, call.message.chat.id)
    return state is UserInfoState.date_of_entry

def filter_func_departure_date(call: CallbackQuery) -> bool:
    state = bot.get_state(call.from_user.id, call.message.chat.id)
    return state is UserInfoState.departure_date

@bot.callback_query_handler(func=filter_func_entry_date)
def process_dates(call: CallbackQuery) -> None:
    result, key, step = DetailedTelegramCalendar(locale='ru', min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выберите {LSTEP_RU[step]}', call.message.chat.id,
                              call.message.message_id, reply_markup=key)
    else:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['date_of_entry'] = result
        bot.set_state(call.from_user.id, UserInfoState.departure_date, call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Введите дату выселения')
        run_calendar(call.from_user.id, result)

@bot.message_handler(state=UserInfoState.departure_date)
def departure_date(message: Message) -> None:
    bot.reply_to(message, 'Пожалуйста, нажмите на кнопку.')

@bot.callback_query_handler(func=filter_func_departure_date)
def process_dates(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        result, key, step = DetailedTelegramCalendar(locale='ru', min_date=data['date_of_entry']).process(call.data)
        if not result and key:
            bot.edit_message_text(f'Выберите {LSTEP_RU[step]}', call.message.chat.id,
                                  call.message.message_id, reply_markup=key)
        else:
            data['departure_date'] = result
            if data['command'] == 'bestdeal':
                bot.set_state(call.from_user.id, UserInfoState.min_price, call.message.chat.id)
                bot.send_message(call.message.chat.id, 'Введите минимальную стоимость за ночь (целое число), $')
            else:
                bot.set_state(call.from_user.id, UserInfoState.number_of_hotels, call.message.chat.id)
                bot.send_message(call.message.chat.id, 'Введите количество отелей (не более 20)')

@bot.message_handler(state=UserInfoState.min_price)
def min_price(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price'] = int(message.text)
        bot.set_state(message.from_user.id, UserInfoState.max_price, message.chat.id)
        bot.send_message(message.chat.id, 'Введите максимальную стоимость за ночь (целое число), $')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте только цифры')

@bot.message_handler(state=UserInfoState.max_price)
def max_price(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['min_price'] > int(message.text):
                bot.send_message(message.chat.id, 'Максимальная стоимость за ночь не может быть меньше минимальной,'
                                                  ' попробуйте ещё раз.')
            else:
                data['max_price'] = int(message.text)
                bot.set_state(message.from_user.id, UserInfoState.min_dist, message.chat.id)
                bot.send_message(message.chat.id, 'Введите минимальное расстояние до центра города (целое число)')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте только цифры')

@bot.message_handler(state=UserInfoState.min_dist)
def min_dist(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_dist'] = int(message.text)
        bot.set_state(message.from_user.id, UserInfoState.max_dist, message.chat.id)
        bot.send_message(message.chat.id, 'Введите максимальное расстояние до центра города (целое число)')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте только цифры')

@bot.message_handler(state=UserInfoState.max_dist)
def max_dist(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['min_dist'] > int(message.text):
                bot.send_message(message.chat.id, 'Максимальное расстояние не может быть меньше минимального,'
                                                  'попробуйте ещё раз.')
            else:
                data['max_dist'] = int(message.text)
                bot.set_state(message.from_user.id, UserInfoState.number_of_hotels, message.chat.id)
                bot.send_message(message.chat.id, 'Введите количество отелей (не более 20)')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте только цифры')

@bot.message_handler(state=UserInfoState.number_of_hotels)
def number_of_hotels(message: Message) -> None:
    try:
        if int(message.text) <= 20:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['number_of_hotels'] = int(message.text)
            bot.set_state(message.from_user.id, UserInfoState.photo_hotels, message.chat.id)
            bot.send_message(message.chat.id, 'Показать фотографии отелей?', reply_markup=photo_markup())
        else:
            bot.send_message(message.chat.id, 'Количество отелей должно быть не более 20. Попробуйте ещё раз.')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте только цифры')

@bot.message_handler(state=UserInfoState.photo_hotels)
def photo_hotels(message: Message) -> None:
    bot.reply_to(message, 'Пожалуйста, нажмите на кнопку.')

def filter_photo(call: CallbackQuery) -> bool:
    state = bot.get_state(call.from_user.id, call.message.chat.id)
    return state is UserInfoState.photo_hotels

@bot.callback_query_handler(func=filter_photo)
def callback_query(call: CallbackQuery) -> None:
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['answer_photo'] = call.data
        if data['answer_photo'] == 'Да':
            bot.set_state(call.from_user.id, UserInfoState.number_of_photo, call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Сколько фотографий показать? (не более 10)')
        else:
            bot.set_state(call.from_user.id, UserInfoState.find_hotels, call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Идёт поиск отелей...')
            if data['command'] == 'bestdeal':
                find_hotels_bestdeal(call.message.chat.id, data['destination_id'], data['date_of_entry'],
                            data['departure_date'], data['number_of_hotels'],
                            bestdeal_params=bestdeal_params(call.from_user.id, call.message.chat.id))
            else:
                find_hotels(call.message.chat.id, data['destination_id'], data['date_of_entry'],
                        data['departure_date'], data['number_of_hotels'], data['command'])

def bestdeal_params(user_id: int, chat_id: int) -> dict:
    with bot.retrieve_data(user_id, chat_id) as data:
        bestdeal_params = {}
        bestdeal_params['min_price'] = data['min_price']
        bestdeal_params['max_price'] = data['max_price']
        bestdeal_params['min_dist'] = data['min_dist']
        bestdeal_params['max_dist'] = data['max_dist']

        return bestdeal_params

@bot.message_handler(state=UserInfoState.number_of_photo)
def number_of_photo(message: Message) -> None:
    try:
        num_photo = int(message.text)
        if num_photo <= 10:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['number_of_photo'] = int(message.text)
            bot.set_state(message.from_user.id, UserInfoState.find_hotels, message.chat.id)
            bot.send_message(message.chat.id, 'Идёт поиск отелей...')
            if data['command'] == 'bestdeal':
                find_hotels_bestdeal(message.chat.id, data['destination_id'], data['date_of_entry'],
                            data['departure_date'], data['number_of_hotels'],
                            num_photo, bestdeal_params(message.from_user.id, message.chat.id))
            else:
                find_hotels(message.chat.id, data['destination_id'], data['date_of_entry'],
                        data['departure_date'], data['number_of_hotels'], data['command'], num_photo)
        else:
            bot.send_message(message.chat.id, 'Количество фотографий должно быть не более 10. Попробуйте ещё раз.')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, используйте только цифры')

