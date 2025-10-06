from http import HTTPStatus

from celery import chain, group, shared_task
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger

from api.models import Anime

logger = get_task_logger(__name__)


@shared_task
def fetch_anime(start=1, end=20):
    for i in range(start, end + 1):
        chain(
            process_and_store_anime.s(i),
            group(process_and_store_characters.s(), process_and_store_episodes.s()),
        ).delay()


@shared_task(
    max_retries=6,
    autoretry_for=(TimeoutError,),
    retry_jitter=True,
    retry_backoff=True,
    rate_limit='20/m',
)
def process_and_store_anime(anime_id: int):
    from api.serializers import AnimeExternalCreateSerializer
    from api.utils import fetch_anime

    payload, status = fetch_anime(anime_id)

    if status == HTTPStatus.NOT_FOUND:
        raise Ignore()
    elif status == HTTPStatus.TOO_MANY_REQUESTS:
        logger.warning(f'MAL Id {anime_id} | Rate limit reached')
        raise TimeoutError()

    serializer = AnimeExternalCreateSerializer(data=payload)
    if serializer.is_valid():
        anime = serializer.save()
        logger.info(f'MAL Id {anime_id} | Saved')
        return anime.id
    else:
        logger.error(f'MAL Id {anime_id} | Validation error: {serializer.errors}')
        raise Ignore()


@shared_task(
    max_retries=6,
    autoretry_for=(TimeoutError,),
    retry_jitter=True,
    retry_backoff=True,
    rate_limit='15/m',
)
def process_and_store_characters(anime_id):
    from api.serializers import CharacterExternalCreateSerializer
    from api.utils import fetch_anime

    anime = Anime.objects.get(pk=anime_id)
    payload, status = fetch_anime(f'{anime.mal_id}/characters/')

    if status == HTTPStatus.NOT_FOUND:
        raise Ignore()
    elif status == HTTPStatus.TOO_MANY_REQUESTS:
        logger.warning(f'MAL Id {anime.mal_id} Rate limit reached for characters')
        raise TimeoutError()

    serializer = CharacterExternalCreateSerializer(data=payload, many=True, context={'anime': anime})
    if serializer.is_valid():
        serializer.save()
        logger.info(f'MAL Id {anime.mal_id} Characters Saved')
    else:
        logger.error(f'MAL Id {anime.mal_id} for characters | Validation error: {serializer.errors}')


@shared_task(
    max_retries=6,
    autoretry_for=(TimeoutError,),
    retry_jitter=True,
    retry_backoff=True,
    rate_limit='15/m',
)
def process_and_store_episodes(anime_id):
    from api.serializers import EpisodeExternalCreateSerializer
    from api.utils import fetch_anime

    anime = Anime.objects.get(pk=anime_id)
    payload, status = fetch_anime(f'{anime.mal_id}/episodes/')

    if status == HTTPStatus.NOT_FOUND:
        raise Ignore()
    elif status == HTTPStatus.TOO_MANY_REQUESTS:
        logger.warning(f'MAL Id {anime.mal_id} Rate limit reached for episodes')
        raise TimeoutError()

    serializer = EpisodeExternalCreateSerializer(data=payload, many=True, context={'anime': anime})
    if serializer.is_valid():
        serializer.save()
        logger.info(f'MAL Id {anime.mal_id} Episodes Saved')
    else:
        logger.error(f'MAL Id {anime.mal_id} for episode | Validation error: {serializer.errors}')
