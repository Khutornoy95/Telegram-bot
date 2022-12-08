import requests
import json
from config_data import config

url = 'https://hotels4.p.rapidapi.com/locations/v3/search'
headers = {'X-RapidAPI-Key': config.RAPID_API_KEY,
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

    print(json.dumps(data, indent=4))
    print(possible_cities)
    return possible_cities

