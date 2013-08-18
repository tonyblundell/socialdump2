import datetime
from django.db import models
from django.db.models import Q
from django.utils.text import capfirst
from django.utils.timezone import utc
import feedparser
from time import mktime

class Feed(models.Model):
    feed_url = models.URLField(verbose_name='Feed URL')
    icon = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    tz_offset = models.IntegerField(default=0)
    order = models.PositiveIntegerField()
    site_url = models.URLField(verbose_name='Site URL')
    strip_string = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.label

    def pull(self):
        """
            Download the RSS feed, add/update posts.
        """
        for entry in feedparser.parse(self.feed_url).entries:
            try:
                self.parse_feedparser_entry(entry)
            except AttributeError:
                pass # Couldn't add entry as it was incomplete

    def parse_feedparser_entry(self, entry):
        """
            Parse a feedparser entry object to a post object.
        """
        uid = getattr(entry, 'id', None) or entry.link
        posted = datetime.datetime(*entry.published_parsed[:6])
        posted = posted + datetime.timedelta(seconds=self.tz_offset*60*60) 
        text = capfirst(entry.title.replace(self.strip_string, ''))

        url = entry.link

        # If the post already exists, update it 
        qs = self.posts.filter(Q(uid=uid) | Q(text=text))
        if qs:
            post = qs[0]
            post.posted = posted
            post.text = text
            post.url = url
            post.save()
            return

        # Otherwise create a new post 
        self.posts.create(feed=self, uid=uid, posted=posted, text=text, url=url)

class Post(models.Model):
    feed = models.ForeignKey(Feed, related_name='posts')
    posted = models.DateTimeField()
    text = models.TextField()
    uid = models.CharField(max_length=200, verbose_name='UID')
    url = models.URLField(verbose_name='URL')

    class Meta:
        ordering = ('-posted',)

    def __unicode__(self):
        return self.text

    def ago(self):
        now = datetime.datetime.utcnow()
        diff = now - self.posted
        if diff.total_seconds() >= 60:
            periods = (
                ('year', diff.days/365),
                ('month', diff.days/30),
                ('week', diff.days/7),
                ('day', diff.days),
                ('hour', diff.seconds/3600),
                ('minute', diff.seconds/60),
            )
            for label, period in periods:
                if period > 0:
                    if period > 1:
                        label += 's'
                    return '{0} {1} ago'.format(period, label)
        return 'Just now'
