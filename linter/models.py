""" Models for saving news clippings to the database. """

from django.db import models
from django.forms import ModelForm
from django.utils import timezone


PUBLICATIONS = (
    ('Other', 'Other'),
    ('Breitbart', 'Breitbart'),
    ('Daily Kos', 'Daily Kos'),
    ('Firedoglake', 'Firedoglake'),
    ('FOX News', 'FOX News'),
    ('InfoWars.com', 'InfoWars.com'),
    ('Huffington Post', 'Huffington Post'),
    ('Los Angeles Times', 'Los Angeles Times'),
    ('New York Times', 'New York Times'),
    ('The Blaze', 'The Blaze'),
    ('Washington Post', 'Washington Post')
)


class Clipping(models.Model):

    """ Model for saving a news clipping -- sans scoring. """

    title = models.CharField(max_length=255, default='', blank=True)
    publication = models.CharField(max_length=255, choices=PUBLICATIONS, default='', blank=True)
    author = models.CharField(max_length=255, default='', blank=True)
    url = models.CharField(max_length=255, default='', blank=True)
    content = models.TextField(default='')
    published = models.DateTimeField('date published', default=timezone.now(), blank=True)
    added = models.DateTimeField('date added by user', default=timezone.now(), blank=True, auto_now_add=True)

    def __unicode__(self):
        return self.title


class ClippingForm(ModelForm):

    """ A form for the Clipping model to test against in Django. """

    class Meta:
        model = Clipping


# event log class?
# see https://developers.google.com/news-search/v1/jsondevguide#basic_query
# https://github.com/rowanmanning/joblint
