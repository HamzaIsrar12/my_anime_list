from django.core.management.base import BaseCommand, CommandError

from api.tasks import fetch_anime


class Command(BaseCommand):
    help = '''
    Fetches anime data from third-party API
    
    Start Celery Worker: celery -A myanimelist worker --concurrency=1 -l INFO
    Start Redis Sever: redis-server
    
    '''

    def add_arguments(self, parser):
        parser.add_argument('--start', type=int, default=1)
        parser.add_argument('--end', type=int, default=20)

    def handle(self, *args, **options):
        start = options['start']
        end = options['end']

        if start < 1:
            raise CommandError('--start must be >= 1')
        if end < start:
            raise CommandError('--end must be >= --start')

        try:
            fetch_anime.delay(start, end)
        except Exception as e:
            raise CommandError(f'Could not fetch anime data from third-party API: {e}')
