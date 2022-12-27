import requests
from config_data import config

def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"
    headers = {"content-type": "application/json",
               'X-RapidAPI-Key': config.RAPID_API_KEY,
               'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'}

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params,
            headers=headers
        )
    else:
        return post_request(
            url=url,
            params=params,
            headers=headers
        )


def get_request(url, params, headers):
    try:
        response = requests.request('GET', url, headers=headers, params=params, timeout=15)
        if response.status_code == requests.codes.ok:
            return response.text
    except:
        pass

def post_request(url, params, headers):
    try:
        response = requests.request("POST", url, json=params, headers=headers, timeout=15)
        if response.status_code == requests.codes.ok:
            return response.text
    except:
        pass