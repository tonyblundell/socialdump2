from django.core.management.base import BaseCommand, CommandError
import logging
from main.models import Feed

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        for feed in feeds:
            try:
                feed.pull()
            except:
                logging.exception('Error pulling feed {0}'.format(feed))
