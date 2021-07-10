from urllib.error import URLError
from django.core.management.base import BaseCommand, CommandError
from feed.models import Feed


class Command(BaseCommand):
    help = 'Creates new feed and loads new articles'

    def add_arguments(self, parser):
        parser.add_argument('link', nargs='+', type=str)

    def handle(self, *args, **options):
        for link in options['link']:
            try:
                feed = Feed.objects.create_feed(link)
            except URLError:
                raise CommandError(
                    f'Link * {link} * is not valid rss source or network problem occured')

            self.stdout.write(self.style.SUCCESS(
                f'Successfully created feed * {feed.title} * '))
