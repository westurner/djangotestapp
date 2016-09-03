
"""
djangotestapp.tagbrowser.models
"""
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
# from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import Group


# from taggit.managers import TaggableManager

from .fields import JSONField_odict
from ..utils import get_uuid4_hex


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid4_hex, editable=False)
    url = models.URLField(db_index=True)
    name = models.TextField(db_index=True)
    description = models.TextField(db_index=True)
    description_html = models.TextField(db_index=False, null=True, blank=True)
    data = JSONField_odict(null=True)
    context_url = models.URLField()
    context = JSONField_odict(null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,
                             related_name='resources')
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

    # likeCount = models.IntegerField(default=0)
    # hashtags = models.ManyToManyField(Hashtag, blank=True)
    # tags = TaggableManager()

    @property
    def name(self):
        return self.url

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resource_detail_view', pk=str(self.id))


class ResourceEdgeType(models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid4_hex, editable=False)
    name = models.TextField(db_index=True)

    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)

class ResourceEdge(models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid4_hex, editable=False)

    type = models.ManyToManyField(ResourceEdgeType, related_name="edges")
    source = models.ManyToManyField(Resource, related_name="edges_out")
    dest = models.ManyToManyField(Resource, related_name="edges_in")

    data = models.ForeignKey(Resource)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True,
                             related_name='resource_edges')
    group = models.ForeignKey(Group)

    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)


# class ResourceEdgeNaieve(models.Model):
#     source = models.ForeignKey(Resource)
#     dest = models.ForeignKey(Resource)
#     data = models.ForeignKey(Resource)

