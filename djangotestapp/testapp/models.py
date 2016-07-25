
"""
djangotestapp.testapp.models
"""
from __future__ import unicode_literals

import itertools

from django.conf import settings
from django.core.urlresolvers import reverse
# from django.contrib.auth import get_user_model
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

        # PRF: minimize get_or_create queries
        if len(computed['hashtags']) == 1:
            hashtag, created = Hashtag.objects.get_or_create(
                name=computed['hashtags'][0])
            self.hashtags.add(hashtag)
        elif len(computed['hashtags']) > 1:
            existing_hashtags = Hashtag.objects.filter(name__in=computed['hashtags'])
            new_hashtag_names = set.difference(set(computed['hashtags']), set(t.name for t in existing_hashtags))
            new_hashtags = []
            for hashtag_name in new_hashtag_names:
                # get_or_create here because otherwise
                # there could be a race condition
                # where a different query has already created the given hashtag
                hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
                new_hashtags.append(hashtag)
            self.hashtags.add(*itertools.chain(existing_hashtags, new_hashtags))

        users_by_name = computed['users_by_name']
        if users_by_name is not None:
            self.users.add(*users_by_name.values())
        return super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return self.articleBody

    def get_absolute_url(self):
        return reverse('message_detail_view',
                       kwargs=dict(username=str(self.user), pk=str(self.id)))

    def get_user_absolute_url(self):
        return reverse('message_user_list_view',
                       kwargs=dict(username=self.user))
