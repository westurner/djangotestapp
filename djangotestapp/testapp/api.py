
"""
djangotestapp.testapp.api
"""
from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets

from djangotestapp.testapp import models

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'username',)
        extra_kwargs = {
            'url': {'lookup_field': 'username'},
        }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'


class HashtagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Hashtag
        fields = (
            'url',
            'name',)
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class HashtagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Hashtag.objects.all()
    serializer_class = HashtagSerializer
    lookup_field = 'name'
    lookup_url_kwarg = 'name'


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    users = UserSerializer(many=True)
    # serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    hashtags = HashtagSerializer(many=True)
    # serializers.HyperlinkedRelatedField(many=True, view_name='hashtag-detail', read_only=True)
    class Meta:
        model = models.Message
        depth = 1
        fields = (
            'user',
            'articleBody',
            'articleBody_html',
            'dateCreated',
            'dateModified',
            'likeCount',

            'hashtags',
            'users',
        )
        read_only_fields = (
            'user',
            'articleBody_html',
            'dateCreated',
            'dateModified',
            'likeCount',

            'hashtags',
            'users',
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = MessageSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hashtags', HashtagViewSet)
router.register(r'messages', MessageViewSet)
