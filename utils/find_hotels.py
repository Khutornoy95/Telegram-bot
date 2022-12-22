from loader import bot
import requests
import json
from config_data import config
from telebot import types
import requests


def find_hotels(chat_id, destination_id, check_in, check_out, resultsSize, num_photo=None):


    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": destination_id},
        "checkInDate": {
            "day": int(check_in.strftime('%Y%m%d')[-2::]),
            "month": int(check_in.strftime('%Y%m%d')[4:6:]),
            "year": int(check_in.strftime('%Y%m%d')[:4:])
        },
        "checkOutDate": {
            "day": int(check_out.strftime('%Y%m%d')[-2::]),
            "month": int(check_out.strftime('%Y%m%d')[4:6:]),
            "year": int(check_out.strftime('%Y%m%d')[:4:])
        },
        "rooms": [
            {"adults": 1}
        ],
        "resultsStartingIndex": 0,
        "resultsSize": resultsSize,
        "sort": "PRICE_HIGH_TO_LOW",
        # "sort": "PRICE_LOW_TO_HIGH",
        "filters": {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8508e118a7msh0417a18b41302b0p146d1bjsn9ea1996d58fe",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    if response:
        parsed = json.loads(response.text)
        hotels = []
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        for elem in parsed['data']['propertySearch']['properties']:
            hotels.append(dict())
            hotels[-1]['id'] = elem['id']
            hotels[-1]['name'] = elem['name']
            hotels[-1]['distance_info'] = str(elem['destinationInfo']['distanceFromDestination']['value'])
            price = elem['price']['displayMessages'][1]['lineItems'][0]['value']
            total_price = ''
            for elem in price:
                if not elem.isalpha():
                    total_price += elem
            hotels[-1]['total_price'] = total_price

            payload = {
                "currency": "USD",
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "propertyId": hotels[-1]['id']
            }

            hotel_response = requests.request("POST", url, json=payload, headers=headers)
            if hotel_response:
                parsed_hotel = json.loads(hotel_response.text)
                hotels[-1]['address'] = parsed_hotel['data']['propertyInfo']['summary']['location']['address']['addressLine']
                if num_photo:
                    hotels[-1]['photo'] = []
                    for photo_id in range(num_photo):
                        hotels[-1]['photo'].append(parsed_hotel['data']['propertyInfo']['propertyGallery']['images'][photo_id]['image']['url'])



        for hotel in hotels:
            hotel_info = 'Название: ' + hotel['name'] + '\nАдрес: ' + \
                         hotel['address'] + '\nРасстояние до центра города, км: ' + \
                         hotel['distance_info'] + '\nСтоимость проживания: ' + hotel['total_price']
            bot.send_message(chat_id, hotel_info)
            if num_photo:
                media = []
                for url in hotel['photo']:
                    photo = types.InputMediaPhoto(url)
                    media.append(photo)
                bot.send_media_group(chat_id, media)

