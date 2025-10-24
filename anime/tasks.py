import requests
from celery import shared_task
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.core.exceptions import BadRequest
from django.utils.dateparse import parse_datetime
from rest_framework import status

from anime.choices import Season
from anime.models import Anime, Genre, Studio
from core.constants import BASE_URL, CACHE_TTL, CACHED_PAGE_FETCH_LIMIT, LIVE_PAGE_FETCH_LIMIT
from media.choices import ImageType
from media.models import Image

logger = get_task_logger(__name__)


@shared_task(
    max_retries=1,
    autoretry_for=(TimeoutError,),
    retry_jitter=True,
    retry_backoff=True,
    rate_limit='20/m',
)
def search_external_anime(anime_name: str, page: int = 1):
    cache_key = f'search_external_anime:{anime_name}:{page}'
    if cache.get(cache_key) and page <= CACHED_PAGE_FETCH_LIMIT:
        logger.info(f'Cached external anime for page {page}')
        search_external_anime.delay(anime_name, page + 1)
        return

    url = f'{BASE_URL}?q={anime_name}&page={page}'
    logger.info(f'Search external anime at {url}')

    try:
        response = requests.get(url)
    except BadRequest:
        logger.warning(f'Bad Request')
        raise Ignore()
    except Exception:
        raise Ignore()

    if response.status_code != status.HTTP_200_OK:
        logger.warning(f'Response status {response.status_code}')
        raise Ignore()

    payload = response.json() or {}
    data = payload.get('data') or []

    created_any = False

    for item in data:
        title = item.get('title')
        synopsis = item.get('synopsis')
        rating = item.get('rating')

        if not (synopsis and rating and title):
            continue

        mal_id = item.get('mal_id')
        url = item.get('url')
        season = Season.value_of(item.get('season'))
        aired_from, aired_till = get_airing_date(item.get('aired'))

        anime, created = Anime.objects.update_or_create(
            mal_id=mal_id,
            defaults={
                'title': title,
                'url': url,
                'synopsis': synopsis,
                'rating': rating,
                'season': season,
                'aired_from': aired_from,
                'aired_till': aired_till,
            },
        )

        if created:
            created_any = True
            anime.images.set(_get_image_models(item.get('images')))
            anime.studios.set(_get_studio_models(item.get('studios')))
            anime.genres.set(_get_genre_models(item.get('genres')))

        cache.set(cache_key, True, timeout=CACHE_TTL)

    if not created_any and page < LIVE_PAGE_FETCH_LIMIT:
        search_external_anime.delay(anime_name, page + 1)


def _get_image_models(images_data):
    image_models = []
    for image_type, urls in images_data.items():
        image, _ = Image.objects.update_or_create(
            type=ImageType.value_of(image_type),
            image_url=urls.get('image_url'),
            defaults={
                'small_image_url': urls.get('small_image_url', None),
                'large_image_url': urls.get('large_image_url', None),
            }
        )
        image_models.append(image)

    return image_models


def _get_studio_models(studios_data):
    studio_models = []
    for studio_data in studios_data:
        mal_id = studio_data.get('mal_id')
        name = studio_data.get('name')
        url = studio_data.get('url')
        studio, _ = Studio.objects.update_or_create(
            mal_id=mal_id,
            defaults={
                'name': name,
                'url': url,
            }
        )
        studio_models.append(studio)

    return studio_models


def _get_genre_models(genres_data):
    genre_models = []
    for genre_data in genres_data:
        mal_id = genre_data.get('mal_id')
        name = genre_data.get('name')
        url = genre_data.get('url')
        genre, _ = Genre.objects.update_or_create(
            mal_id=mal_id,
            defaults={
                'name': name,
                'url': url,
            }
        )
        genre_models.append(genre)

    return genre_models


def get_airing_date(aired_data):
    aired_from = aired_data.get('from', None)
    aired_till = aired_data.get('to', None)

    if aired_from:
        aired_from = parse_datetime(aired_from)
    if aired_till:
        aired_till = parse_datetime(aired_till)

    return aired_from, aired_till
