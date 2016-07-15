
import unittest

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from .utils import linkify_articlebody

LINKIFY_TESTDATA = [{
    'user': 'abc',
    'articleBody': '@to #hashtag message',
    'articleBody_html': "<a class='usertag' href='/@to'>@to</a> <a class='hashtag' href='/tag/hashtag'>#hashtag</a> message"},
]


class TestUtils(unittest.TestCase):
    def test_linkify_articlebody(self):
        testdata = LINKIFY_TESTDATA[0]
        output = linkify_articlebody(testdata['articleBody'])
        self.assertEqual(output, testdata['articleBody_html'])


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
from djangotestapp.testapp.models import Message


class TestTestappModels(TestCase):
    def test_Message_0(self):
        testdata_ = LINKIFY_TESTDATA[0]
        testdata = testdata_.copy()
        testdata.pop('articleBody_html')
        m = Message(**testdata)
        self.assertTrue(isinstance(m, Message))
        self.assertEqual(m.user, testdata['user'])
        self.assertEqual(m.articleBody, testdata['articleBody'])

        m.save()
        m_pk = m.pk
        m2 = Message.objects.get(pk=m_pk)
        self.assertTrue(isinstance(m2, Message))
        self.assertEqual(m2.user, testdata['user'])
        self.assertEqual(m2.articleBody, testdata['articleBody'])
        self.assertEqual(m2.articleBody_html, testdata_['articleBody_html'])

        m.delete()
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Message.objects.get(pk=m_pk)
