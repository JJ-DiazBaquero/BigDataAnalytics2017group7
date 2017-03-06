from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import datetime

@python_2_unicode_compatible
class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_description = models.TextField()
    post_published_date = models.DateTimeField('date published')
    post_link = models.CharField(max_length=400)

    def __str__(self):
        return self.post_title