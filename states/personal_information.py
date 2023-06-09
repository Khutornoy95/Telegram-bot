from telebot.handler_backends import State, StatesGroup
class UserInfoState(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()
    input_city = State()
    buttons_city = State()
    date_of_entry = State()
    departure_date = State()
    number_of_hotels = State()
    photo_hotels = State()
    number_of_photo = State()
    find_hotels = State()
    min_price = State()
    max_price = State()
    min_dist = State()
    max_dist = State()