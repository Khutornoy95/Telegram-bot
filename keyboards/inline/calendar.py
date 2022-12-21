from telegram_bot_calendar import DetailedTelegramCalendar
from loader import bot
from datetime import date

LSTEP_RU: dict[str, str] = {'y': 'год', 'm': 'месяц', 'd': 'день'}

def run_calendar(user_id, min_date=date.today()):
    calendar, step = DetailedTelegramCalendar(min_date=min_date).build()
    bot.send_message(user_id, f'Выберите {LSTEP_RU[step]}', reply_markup=calendar)


