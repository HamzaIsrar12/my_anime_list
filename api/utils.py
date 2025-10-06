from http import HTTPStatus

import requests

BASE_URL = 'https://api.jikan.moe/v4/anime'


def fetch_anime(path):
    response = requests.get(f'{BASE_URL}/{path}/')

    if response.status_code == HTTPStatus.OK:
        return response.json().get('data'), HTTPStatus.OK
    elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return {}, HTTPStatus.TOO_MANY_REQUESTS
    else:
        return {}, HTTPStatus.NOT_FOUND
