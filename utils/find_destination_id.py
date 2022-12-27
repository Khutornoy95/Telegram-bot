import requests
import json
from config_data import config

url = 'https://hotels4.p.rapidapi.com/locations/v3/search'
headers = {"content-type": "application/json",
           'X-RapidAPI-Key': config.RAPID_API_KEY,
           'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'}

def destination_id(city):

    querystring = {'q': city, 'locale': 'ru_RU'}
    response = requests.request('GET', url, headers=headers, params=querystring, timeout=10)
    if response:
        data = json.loads(response.text)
        possible_cities = {}
        for elem in data["sr"]:
            if elem['type'] == 'CITY' or elem['type'] == 'NEIGHBORHOOD':
                possible_cities[elem['gaiaId']] = elem['regionNames']['fullName']

    return possible_cities


#api_request(locations/v3/search, {'q': data['input_city'], 'locale': 'ru_RU'}, 'GET')