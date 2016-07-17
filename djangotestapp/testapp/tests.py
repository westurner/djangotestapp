
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

    def test_Message_1(self):
        testdata_ = LINKIFY_TESTDATA[0]
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
