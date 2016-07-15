
from django.test import Client, TestCase


class TestTestappSimpleViews(TestCase):
    def test_simple_view(self):
        c = Client()
        r = c.get('/')
        self.assertContains(r, 'simple view')
        self.assertHTMLEqual(r.content, '<h1>simple view</h1>')


import django.core.exceptions as exceptions
from djangotestapp.testapp.models import Message


class TestTestappModels(TestCase):
    def test_Message_0(self):
        testdata = dict(user='abc', articleBody='xyz')
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

        m.delete()
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            m3 = Message.objects.get(pk=m_pk)
            m3
