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

import djangotestapp.testapp.views as views
import djangotestapp.testapp.api as api
import djangotestapp.testapp.search_views as search_views

urlpatterns = [
    url(r'^$', views.MessageListView.as_view(), {'title': 'testapp'}, name='message_list_view'),
    url(r'^test/simple', views.simple_view, name='simple_view'),
    url(r'^new', views.MessageCreateView.as_view(), name='message_create_view'),
    url(r'^@(?P<username>[\w\d]+)/(?P<pk>\d+)', views.MessageDetailView.as_view(), name='message_detail_view'),
    url(r'^me', views.MeRedirectView.as_view(), name='me_redirect_view'),
    url(r'^@(?P<username>[\w\d]+)', views.MessageUserListView.as_view(), name='message_user_list_view'),
    url(r'^tag/(?P<hashtag>[\w\d]+)', views.HashtagListView.as_view(), name='hashtag_list_view'),
    url(r'^@/(?P<username>[\w\d]+)/tag/(?P<hashtag>[\w\d]+)', views.MessageUserHashtagListView.as_view(), name='message_user_hashtag_list_view'),

    url(r'^search_/', search_views.TestSearchView.as_view(), name='test_search'),

    url(r'^api/v1/', include(api.router.urls)),
]
