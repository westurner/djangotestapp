"""djangotestapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

import testapp.views

urlpatterns = [
    url(r'^$', testapp.views.MessageListView.as_view(), {'title': 'testapp'}, name='message_list_view'),
    url(r'^test/simple', testapp.views.simple_view, name='simple_view'),
    url(r'^new', testapp.views.MessageCreateView.as_view(), name='message_create_view'),
    url(r'^@(?P<username>[\w\d]+)/(?P<pk>\d+)', testapp.views.MessageDetailView.as_view(), name='message_detail_view'),
    url(r'^me', testapp.views.MeRedirectView.as_view(), name='me_redirect_view'),
    url(r'^@(?P<username>[\w\d]+)', testapp.views.MessageUserListView.as_view(), name='message_user_list_view'),
    url(r'^tag/(?P<hashtag>[\w\d]+)', testapp.views.HashtagListView.as_view(), name='hashtag_list_view'),
    url(r'^@/(?P<username>[\w\d]+)/tag/(?P<hashtag>[\w\d]+)', testapp.views.MessageUserHashtagListView.as_view(), name='message_user_hashtag_list_view'),

    url(r'^auth-api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),

    url(r'^admin/', admin.site.urls),
]
