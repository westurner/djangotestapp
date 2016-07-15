
from django.test import Client, TestCase


class TestTestappSimpleViews(TestCase):
    def test_simple_view(self):
        c = Client()
        r = c.get('/')
        self.assertContains(r, 'simple view')
        self.assertHTMLEqual(r.content, '<h1>simple view</h1>')

from djangotestapp.testapp.models import Message
class TestTestappModels(TestCase):
    def test_models_0(self):
        testdata = dict(user='abc', message='xyz')
        m = Message(**testdata)
        self.assertTrue(isinstance(m, Message))
        self.assertEqual(m.user, testdata['user'])
        self.assertEqual(m.message, testdata['message'])
