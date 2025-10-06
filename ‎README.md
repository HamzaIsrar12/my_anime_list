# MyAnimeList

A Django REST Framework project inspired by **MyAnimeList**, exposing APIs that mirror MAL resources.

## Setup

1. Clone the repo
2. Install requirements
3. Configure database in `.env` (see `.env.example`)
4. Run the app

## Populate Database

The management command enqueues **Celery** tasks that prefetch data from MyAnimeList.

1. Start Redis

```bash
    redis-server
```

2. Start Celery (single worker to respect third-party throttling)

```bash
    celery -A myanimelist worker --concurrency=1 -l INFO
```

3. Run the fetch command

```bash
    python manage.py fetch_anime
```

## API Docs

Browse interactive docs at:

```bash
    <base-url>/api/docs/
```

## Project Layout

* `core/` — base/shared layer (abstract models)
* `api/` — domain/API layer (models, serializers, views, permissions, routers)

## Upcoming

* Deployment on AWS (service hosting, managed DB, Redis)
