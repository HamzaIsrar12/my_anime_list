import logging
from http import HTTPStatus

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils.dateparse import parse_datetime

from anime.choices import Season
from anime.models import Anime, Genre, Studio
from core.services import JikanService
from media.choices import ImageType
from media.models import Image

logger = logging.getLogger(__name__)


class AnimeDataService:

    @classmethod
    def search_external_anime(cls, search_query: str, page: int = 1, timeout: int = 5):
        if page > settings.SEARCH_PAGE_FETCH_LIMIT:
            return

        page_cache_key = f'external_search:{search_query}:{page}'
        if cache.get(page_cache_key):
            cls.search_external_anime(search_query, page + 1, timeout)
            return

        data, status = JikanService.get_anime_list(
            params={'q': search_query, 'page': page},
            timeout=timeout
        )
        if status != HTTPStatus.OK:
            logger.warning(
                msg='Issues while fetching anime data',
                extra={
                    'url': 'get_anime_list',
                    'query': search_query,
                    'page': page,
                    'status': status,
                },
            )
            return
        elif not data:
            logger.info(
                msg='No anime found',
                extra={
                    'url': 'get_anime_list',
                    'query': search_query,
                    'page': page,
                }
            )
            cache.set(page_cache_key, True, timeout=settings.CACHE_TTL)
            return

        valid_items = cls._filter_valid_items(data)
        cls._bulk_upsert(valid_items)

        cache.set(page_cache_key, True, timeout=settings.CACHE_TTL)

    @classmethod
    def _filter_valid_items(cls, data):
        filtered_items = []
        for item in data:
            if item.get('title') and item.get('synopsis') and item.get('rating'):
                filtered_items.append(item)
        return filtered_items

    @classmethod
    def _bulk_upsert(cls, items):
        collection = cls._collect_models_and_links(items)
        cls._bulk_create_models(collection)

        relation_model_maps = cls._load_relation_maps(collection)
        cls._bulk_link_relations(collection, relation_model_maps)

    @classmethod
    def _collect_models_and_links(cls, items):
        anime_by_id = {}
        images_by_key, studios_by_id, genres_by_id = {}, {}, {}
        anime_to_image_keys, anime_to_studio_mal_ids, anime_to_genre_mal_ids = {}, {}, {}

        for item in items:
            mal_id = item.get('mal_id')
            season = Season.value_of(item.get('season'))
            aired_from, aired_till = cls.get_airing_date(item.get('aired'))

            anime_by_id[mal_id] = Anime(
                mal_id=mal_id,
                title=item.get('title'),
                synopsis=item.get('synopsis'),
                rating=item.get('rating'),
                url=item.get('url'),
                aired_from=aired_from,
                aired_till=aired_till,
                season=season,
            )

            studios_data = item.get('studios')
            for studio_data in studios_data:
                studio_id = studio_data.get('mal_id')
                studios_by_id[studio_id] = Studio(
                    mal_id=studio_id,
                    name=studio_data.get('name'),
                    url=studio_data.get('url'),
                )
                anime_to_studio_mal_ids.setdefault(mal_id, set()).add(studio_id)

            genres_data = item.get('genres')
            for genre_data in genres_data:
                genre_id = genre_data.get('mal_id')
                genres_by_id[genre_id] = Genre(
                    mal_id=genre_id,
                    name=genre_data.get('name'),
                    url=genre_data.get('url'),
                )
                anime_to_genre_mal_ids.setdefault(mal_id, set()).add(genre_id)

            images_data = item.get('images')
            for image_type, urls in images_data.items():
                image_type = ImageType.value_of(image_type)
                image_url = urls.get('image_url')
                key = (image_type, image_url)
                images_by_key[key] = Image(
                    type=image_type,
                    image_url=image_url,
                    small_image_url=urls.get('small_image_url', None),
                    large_image_url=urls.get('large_image_url', None),
                )
                anime_to_image_keys.setdefault(mal_id, set()).add(key)

        return {
            'anime_by_id': anime_by_id,
            'images_by_key': images_by_key,
            'studios_by_id': studios_by_id,
            'genres_by_id': genres_by_id,
            'anime_to_image_keys': anime_to_image_keys,
            'anime_to_studio_mal_ids': anime_to_studio_mal_ids,
            'anime_to_genre_mal_ids': anime_to_genre_mal_ids,
        }

    @classmethod
    def _bulk_create_models(cls, collection):
        with transaction.atomic():
            Anime.objects.bulk_create(
                objs=collection['anime_by_id'].values(),
                update_conflicts=True,
                unique_fields=['mal_id'],
                update_fields=['title', 'synopsis', 'rating', 'url', 'season', 'aired_from', 'aired_till'],
            )

            Studio.objects.bulk_create(
                objs=collection['studios_by_id'].values(),
                update_conflicts=True,
                unique_fields=['mal_id'],
                update_fields=['name', 'url'],
            )

            Genre.objects.bulk_create(
                objs=collection['genres_by_id'].values(),
                update_conflicts=True,
                unique_fields=['mal_id'],
                update_fields=['name', 'url'],
            )

            Image.objects.bulk_create(
                objs=collection['images_by_key'].values(),
                ignore_conflicts=True,
            )

    @classmethod
    def _load_relation_maps(cls, collection):
        anime_map = Anime.objects.filter(
            mal_id__in=collection['anime_by_id'].keys()
        ).in_bulk(field_name='mal_id')

        genre_map = Genre.objects.filter(
            mal_id__in=collection['genres_by_id'].keys()
        ).in_bulk(field_name='mal_id')

        studio_map = Studio.objects.filter(
            mal_id__in=collection['studios_by_id'].keys()
        ).in_bulk(field_name='mal_id')

        image_map = {}
        image_urls = [url for _, url in collection['images_by_key'].keys()]
        for img in Image.objects.filter(image_url__in=image_urls):
            image_map[(img.type, img.image_url)] = img

        return {
            'anime_map': anime_map,
            'genre_map': genre_map,
            'studio_map': studio_map,
            'image_map': image_map,
        }

    @classmethod
    def _bulk_link_relations(cls, collection, relation_maps):
        ImagesThrough = Anime.images.through
        StudiosThrough = Anime.studios.through
        GenresThrough = Anime.genres.through

        image_links, studio_links, genre_links = [], [], []

        anime_map = relation_maps['anime_map']
        for mal_id in collection['anime_by_id'].keys():
            parent = anime_map.get(mal_id)
            if not parent:
                continue

            for studio_mal_id in collection['anime_to_studio_mal_ids'].get(mal_id, ()):
                st = relation_maps['studio_map'].get(studio_mal_id)
                if not st:
                    continue
                studio_links.append(StudiosThrough(anime_id=parent.id, studio_id=st.id))

            for genre_mal_id in collection['anime_to_genre_mal_ids'].get(mal_id, ()):
                genre = relation_maps['genre_map'].get(genre_mal_id)
                if not genre:
                    continue
                genre_links.append(GenresThrough(anime_id=parent.id, genre_id=genre.id))

            for key_tuple in collection['anime_to_image_keys'].get(mal_id, ()):
                img = relation_maps['image_map'].get(key_tuple)
                if not img:
                    continue
                image_links.append(ImagesThrough(anime_id=parent.id, image_id=img.id))

        with transaction.atomic():
            ImagesThrough.objects.bulk_create(image_links, ignore_conflicts=True)
            GenresThrough.objects.bulk_create(genre_links, ignore_conflicts=True)
            StudiosThrough.objects.bulk_create(studio_links, ignore_conflicts=True)

    @classmethod
    def get_airing_date(cls, aired_data):
        aired_from = aired_data.get('from', None)
        aired_till = aired_data.get('to', None)

        if aired_from:
            aired_from = parse_datetime(aired_from)
        if aired_till:
            aired_till = parse_datetime(aired_till)

        return aired_from, aired_till
