from http import HTTPStatus
from json import JSONDecodeError

import requests

from core.constants import JIKAN_API_BASE_URL


class JikanService:
    @classmethod
    def get_anime_data(cls, mal_id):
        url = f'{JIKAN_API_BASE_URL}/{mal_id}/'
        return cls._get_result(url)

    @classmethod
    def get_anime_list(cls, params, timeout):
        url = f'{JIKAN_API_BASE_URL}'
        return cls._get_result(url, params, timeout)

    @classmethod
    def get_anime_characters_data(cls, mal_id):
        url = f'{JIKAN_API_BASE_URL}/{mal_id}/characters/'
        return cls._get_result(url)

    @classmethod
    def get_anime_episodes_data(cls, mal_id):
        url = f'{JIKAN_API_BASE_URL}/{mal_id}/episodes/'
        return cls._get_result(url)

    @classmethod
    def _get_result(cls, url, params=None, timeout=None):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                return {}, HTTPStatus.TOO_MANY_REQUESTS

            body = response.json()
            if cls._is_data_valid(body):
                return body.get('data'), HTTPStatus.OK

            return {}, HTTPStatus.NOT_FOUND

        except (JSONDecodeError, ValueError):
            return {}, HTTPStatus.NOT_FOUND
        except requests.RequestException:
            return {}, HTTPStatus.NOT_FOUND

    @staticmethod
    def _is_data_valid(data):
        return data is not None and 'data' in data
