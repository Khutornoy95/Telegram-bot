import requests
import json
import re
from config_data import config

url = 'https://hotels4.p.rapidapi.com/locations/v3/search'
headers = {'X-RapidAPI-Key': config.RAPID_API_KEY,
           'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'}

def destination_id(city):

    querystring = {'q': city, 'locale': 'en_US', 'currency': 'USD'}
    response = requests.request('GET', url, headers=headers, params=querystring, timeout=10)
    data = json.loads(response.text)
    possible_cities = {}
    #for elem in data:
        #print(elem)
    print(json.dumps(data, indent=4))

