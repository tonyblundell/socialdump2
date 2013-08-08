import datetime
from django.db import models
from django.db.models import Q
from django.utils.timezone import utc
import feedparser
from time import mktime

class Feed(models.Model):
    feed_url = models.URLField(verbose_name='Feed URL')
    label = models.CharField(max_length=200)
    order = models.PositiveIntegerField()
    posts_are_links = models.BooleanField(default=False)
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
        print entry.published_parsed
        posted = datetime.datetime(*entry.published_parsed[:6])
        posted = posted.replace(tzinfo=utc)
        text = entry.title.replace(self.strip_string, '')
        text = (text[0] if text.startswith('http') else text[0].upper()) + text[1:]
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

    def posted_ago(self):
        now = datetime.datetime.now(utc)
        print now, now.tzinfo
        print self.posted, self.posted.tzinfo

        diff = now - self.posted
        if diff.total_seconds() > 0:
            periods = (
                (diff.days / 365, 'year'),
                (diff.days / 30, 'month'),
                (diff.days / 7, 'week'),
                (diff.days, 'day'),
                (diff.seconds / 3600, 'hour'),
                (diff.seconds / 60, 'minute'),
            )
            for period, label in periods:
                if period > 0:
                    label = label if period < 2 else label + 's'
                    return '{0} {1} ago'.format(period, label)
        return 'Just now'

