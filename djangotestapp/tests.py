

"""
djangotestapp.tests
"""

import unittest


class TestWSGIApp(unittest.TestCase):
    def test_wsgi_app(self):
        from django.core.handlers.wsgi import WSGIHandler
        from djangotestapp import wsgi
        app = wsgi.application
        self.assertTrue(app)
        self.assertEqual(type(app), WSGIHandler)
