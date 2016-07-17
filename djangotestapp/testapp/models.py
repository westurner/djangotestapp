from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from .utils import linkify_text


class Hashtag(models.Model):
    name = models.TextField(db_index=True, unique=True)
    # count = models.IntegerField(default=0) # TODO: synchronize on delete (premature optimization)

    def __str__(self):
        return u'#{}'.format(self.name)


class Message(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, default=current_user)
    user = models.TextField(db_index=True, max_length=42)
    articleBody = models.TextField(db_index=True, max_length=140)
    articleBody_html = models.TextField(db_index=False, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    likeCount = models.IntegerField(default=0)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def save(self, *args, **kwargs):
        computed = linkify_text(self.articleBody)
        self.articleBody_html = computed['html']
        super(Message, self).save(*args, **kwargs)
        for hashtag in computed['hashtags']:
            ht, created = Hashtag.objects.get_or_create(name=hashtag)
            self.hashtags.add(ht)
        users_by_name = computed['users_by_name']
        if users_by_name is not None:
            for usertag, user in computed['users_by_name'].items():
                self.users.add(user)
        return super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return self.articleBody
