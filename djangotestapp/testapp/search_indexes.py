
from django.contrib.auth import get_user_model
from haystack import indexes

from .models import Hashtag, Message


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    username = indexes.CharField(model_attr='username')

    def get_model(self):
        return get_user_model()

    def index_queryset(self, using=None):
        return self.get_model().objects


class HashtagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Hashtag

    def index_queryset(self, using=None):
        return self.get_model().objects


class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    articleBody = indexes.CharField(model_attr='articleBody')
    articleBody_html = indexes.CharField(model_attr='articleBody_html')
    dateCreated = indexes.DateTimeField(model_attr='dateCreated')
    dateModified = indexes.DateTimeField(model_attr='dateModified')
    likeCount = indexes.IntegerField(model_attr='likeCount')
    hashtags = indexes.MultiValueField()
    users = indexes.MultiValueField()

    def prepare_hashtags(self, obj):
        return [hashtag.name for hashtag in obj.hashtags.all()]
        # TODO: optimize this query

    def prepare_users(self, obj):
        return [user.username for user in obj.users.all()]
        # TODO: optimize this query

    def get_model(self):
        return Message

    def index_queryset(self, using=None):
        return self.get_model().objects
