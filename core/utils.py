from http import HTTPStatus

import requests

from core.constants import BASE_URL


def fetch_anime(path):
    response = requests.get(f'{BASE_URL}/{path}/')
    body = response.json()

    if response.status_code == HTTPStatus.OK and 'data' in body:
        return body.get('data'), HTTPStatus.OK
    elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        return {}, HTTPStatus.TOO_MANY_REQUESTS
    else:
        return {}, HTTPStatus.NOT_FOUND
