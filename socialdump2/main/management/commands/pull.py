from django.core.management.base import BaseCommand, CommandError
from main.models import Feed
import traceback

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        feeds = Feed.objects.all()
        for feed in feeds:
            try:
                feed.pull()
            except:
                traceback.print_exc()
