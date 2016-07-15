
from django.test import Client, TestCase


class TestTestappSimpleViews(TestCase):
    def test_simple_view(self):
        c = Client()
        r = c.get('/')
        self.assertContains(r, 'simple view')
        self.assertHTMLEqual(r.content, '<h1>simple view</h1>')
