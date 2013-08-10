# socialdump2
---
Pulls data from RSS feeds, displays on a home-page.
Requires Django and Feedparser.

Add the following to settings.py:

-   SD2_TITLE = 'My Site Title'
-   SD2_SUBTITLE = 'My Site Subtitle'
-   SD2_MAIL = 'myemail@example.com'

Add feeds via the admin interface at /admin/main/feed.

Run 'python manage.py pull' to pull data.

See tonyblundell.net for an example.
