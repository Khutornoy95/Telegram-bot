from telegram_bot_calendar import DetailedTelegramCalendar
from loader import bot

LSTEP_RU: dict[str, str] = {'y': 'год', 'm': 'месяц', 'd': 'день'}

def run_calendar(message):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.from_user.id, f'Выберите {LSTEP_RU[step]}', reply_markup=calendar)

@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def get_date(call):
    result, key, step = DetailedTelegramCalendar(locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выберите {LSTEP_RU[step]}', call.message.chat.id,
                              call.message.message_id, reply_markup=key)
