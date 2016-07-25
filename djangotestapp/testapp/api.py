
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
            'id',
            'url',
            'username',)
        ## Don't set lookup_field here because usernames can change
        # extra_kwargs = {
        #     'url': {'lookup_field': 'username'},
        # }


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()  # TODO SEC
    serializer_class = UserSerializer
    ## Don't set lookup_field here because usernames can change
    # lookup_field = 'username'
    # lookup_url_kwarg = 'username'


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
    users = UserSerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    class Meta:
        model = models.Message
        depth = 1
        fields = (
            'id',
            'url',
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


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Message.objects.all()  # TODO SEC
    serializer_class = MessageSerializer


class CurrentUserDefault__Username(object):
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user

    def __call__(self):
        return self.user.username

    # CLN: coverage
    # def __repr__(self):
    #     return unicode_to_repr('%s()' % self.__class__.__name__)


class MyMessageSerializer(MessageSerializer):
    user = serializers.HiddenField(
        default=CurrentUserDefault__Username())  # TODO


class MyMessageViewSet(viewsets.ModelViewSet):
    serializer_class = MyMessageSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated():
            return models.Message.objects.none()
        return models.Message.objects.filter(user=user.username)
        # return Message.objects.filter(user__username=user.username) # TODO


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hashtags', HashtagViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mymessages', MyMessageViewSet, 'mymessage')
