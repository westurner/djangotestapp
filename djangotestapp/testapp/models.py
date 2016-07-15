from __future__ import unicode_literals

# from django.conf import settings
from django.db import models

from .utils import linkify_articlebody


class Message(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, default=current_user)
    user = models.TextField(db_index=True, max_length=42)
    articleBody = models.TextField(db_index=True, max_length=140)
    articleBody_html = models.TextField(db_index=False, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    likeCount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.articleBody_html = linkify_articlebody(self.articleBody)
        return super(Message, self).save(*args, **kwargs)
