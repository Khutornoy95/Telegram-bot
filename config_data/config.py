import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('survey', "Передача персональных данных"),
    ('lowprice', 'Вывести список отелей с самой низкой стоимостью проживания'),
    ('highprice', 'Вывести список отелей с самой высокой стоимостью проживания'),
    ('bestdeal', 'Вывести список отелей, наиболее подходящих по цене и расположению от центра'),
    ('history', 'Вывести историю поиска отелей')
)

