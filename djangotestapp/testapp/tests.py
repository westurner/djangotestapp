
import unittest

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from .utils import linkify_text

LINKIFY_TESTDATA = [{
    'user': 'abc',
    'articleBody': '@to #hashtag message',
    'articleBody_html': "<a class='usertag' href='/@to'>@to</a> <a class='hashtag' href='/tag/hashtag'>#hashtag</a> message",
    'hashtags': ['hashtag'],
    'usertags': ['to'],
    }
]

testdata2 = LINKIFY_TESTDATA[0].copy()
testdata2['articleBody_html'] = "@to <a class='hashtag' href='/tag/hashtag'>#hashtag</a> message"
testdata2['usertags'] = []
LINKIFY_TESTDATA.append(testdata2)

LINKIFY_TESTDATA.append({
    'user': 'abc',
    'articleBody': '@to #hashtag #hashtag2 message',
    'articleBody_html': "<a class='usertag' href='/@to'>@to</a> <a class='hashtag' href='/tag/hashtag'>#hashtag</a> <a class='hashtag' href='/tag/hashtag2'>#hashtag2</a> message",
    'hashtags': ['hashtag', 'hashtag2'],
    'usertags': ['to'],
    }
)


class TestUtils(unittest.TestCase):
    def test_linkify_text(self):
        testdata = LINKIFY_TESTDATA[0]
        output = linkify_text(testdata['articleBody'], usernamelookupfn=None)
        self.assertEqual(output['html'], testdata['articleBody_html'])
        self.assertEqual(output['hashtags'], testdata['hashtags'])
        self.assertEqual(output['usertags'], testdata['usertags'])

    def test_linkify_text_no_users(self):
        testdata = LINKIFY_TESTDATA[0]
        testdata['articleBody_html'] = "@to <a class='hashtag' href='/tag/hashtag'>#hashtag</a> message"
        testdata['usertags'] = []
        output = linkify_text(testdata['articleBody'])
        self.assertEqual(output['html'], testdata['articleBody_html'])
        self.assertEqual(output['hashtags'], testdata['hashtags'])
        self.assertEqual(output['usertags'], testdata['usertags'])


class TestTestappRootView(TestCase):
    def test_root_view(self):
        c = Client()
        r = c.get('/')
        self.assertContains(r, '<h1')


class TestTestappSimpleViews(TestCase):
    def test_simple_view(self):
        c = Client()
        r = c.get(reverse('simple_view'))
        self.assertContains(r, 'simple view')
        self.assertHTMLEqual(r.content, '<h1>simple view</h1>')


import django.core.exceptions as exceptions
from djangotestapp.testapp.models import Hashtag, Message


class TestTestappModels(TestCase):

    def test_Hashtag_0(self):
        testdata = {'name': 'test'}
        hashtag = Hashtag(name=testdata['name'])
        self.assertEqual(str(hashtag), '#{}'.format(hashtag.name))
        hashtag.save()
        hashtag_pk = hashtag.pk

        hashtag2 = Hashtag.objects.get(pk=hashtag_pk)
        self.assertEqual(hashtag2.name, testdata['name'])
        self.assertEqual(hashtag, hashtag2)

    def test_Message_0(self):
        testdata_ = LINKIFY_TESTDATA[1]
        testdata = testdata_.copy()
        testdata.pop('articleBody_html')
        testdata.pop('hashtags')
        testdata.pop('usertags')
        m = Message(**testdata)
        self.assertTrue(isinstance(m, Message))
        self.assertEqual(m.user, testdata['user'])
        self.assertEqual(m.articleBody, testdata['articleBody'])
        self.assertEqual(str(m), testdata['articleBody'])

        m.save()
        m_pk = m.pk

        _hashtags = []
        for hashtag in testdata_['hashtags']:
            _hashtag = Hashtag.objects.filter(name=hashtag)
            self.assertEqual(len(_hashtag), 1)
            _hashtags.extend(x for x in _hashtag)
        self.assertEqual(
            set(_hashtags),
            set(m.hashtags.all()))

        m2 = Message.objects.get(pk=m_pk)
        self.assertTrue(isinstance(m2, Message))
        self.assertEqual(m2.user, testdata['user'])
        self.assertEqual(m2.articleBody, testdata['articleBody'])
        self.assertEqual(m2.articleBody_html, testdata_['articleBody_html'])

        m.delete()
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Message.objects.get(pk=m_pk)

    def test_Message_1__one_hashtag(self):
        self.messageTestA(LINKIFY_TESTDATA[0])

    def test_Message_1__two_hashtags(self):
        self.messageTestA(LINKIFY_TESTDATA[2])

    def messageTestA(self, _testdata_):
        testdata_ = _testdata_
        testdata = testdata_.copy()
        testdata.pop('articleBody_html')
        testdata.pop('hashtags')
        testdata.pop('usertags')

        User = get_user_model()
        u = User(username='to')
        u.save()
        self.assertTrue(u.pk)

        m = Message(**testdata)
        self.assertTrue(isinstance(m, Message))
        self.assertEqual(m.user, testdata['user'])
        self.assertEqual(m.articleBody, testdata['articleBody'])

        m.save()
        m_pk = m.pk

        m_url = m.get_absolute_url()
        self.assertEqual(m_url, '/@{}/{}'.format(testdata['user'], m_pk))

        m_user_url = m.get_user_absolute_url()
        self.assertEqual(m_user_url, '/@{}'.format(testdata['user']))

        _hashtags = []
        for hashtag in testdata_['hashtags']:
            _hashtag = Hashtag.objects.filter(name=hashtag)
            self.assertEqual(len(_hashtag), 1)
            _hashtags.extend(x for x in _hashtag)
        self.assertEqual(
            set(_hashtags),
            set(m.hashtags.all()))

        _users = []
        for username in testdata_['usertags']:
            _user = User.objects.filter(username=username)
            self.assertEqual(len(_user), 1)
            _users.extend(x for x in _user)
        self.assertEqual(
            set(_users),
            set(m.users.all()))


        m2 = Message.objects.get(pk=m_pk)
        self.assertTrue(isinstance(m2, Message))
        self.assertEqual(m2.user, testdata['user'])
        self.assertEqual(m2.articleBody, testdata['articleBody'])
        self.assertEqual(m2.articleBody_html, testdata_['articleBody_html'])

        m.delete()
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Message.objects.get(pk=m_pk)


class TestGenericViews(TestCase):
    def test_urls(self):
        c = Client()
        c.get('/')
        c.get(reverse('message_list_view'))

        c.get('/@admin')
        c.get(reverse('message_user_list_view', kwargs=dict(username='admin')))

        c.get('/@admin/1')
        c.get(reverse('message_detail_view', kwargs=dict(username='admin', pk='1')))

        c.get('/@admin/tag/hashtag')
        c.get(reverse('message_user_hashtag_list_view', kwargs=dict(username='admin', hashtag='hashtag')))  # TODO

        c.get('/tag/hashtag')
        c.get(reverse('hashtag_list_view', kwargs=dict(hashtag='hashtag')))

    # def test_me_redirect_notloggedin(self):
    #     c = Client()
    #   resp = c.get('/me', follow=True)
    #   self.assertEqual(resp.redirect_chain[0][0], '/login')

    def test_me_redirect_loggedin(self):
        testdata = dict(username='admin', password='password')
        User = get_user_model()
        u = User(username=testdata['username'], is_active=True)
        u.set_password(testdata['password'])
        u.save()

        c = Client()
        c.login(username=u.username, password=testdata['password'])
        # TODO follow redirect, assert /@admin
        resp = c.get('/me', follow=True)
        self.assertEqual(resp.redirect_chain[0][0], '/@admin')
