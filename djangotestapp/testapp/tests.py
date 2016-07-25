
"""
djangotestapp.testapp.tests
"""

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

    def create_testdata_user(self, testdata):
        # REF: this could just be a minimal fixture
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=testdata['user'], is_active=True)
        user.save()
        testdata['user'] = user
        return user

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
        self.create_testdata_user(testdata)

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
        self.create_testdata_user({'user': 'to'})
        self.messageTestA(LINKIFY_TESTDATA[0])

    def test_Message_1__two_hashtags(self):
        self.create_testdata_user({'user': 'to'})
        self.messageTestA(LINKIFY_TESTDATA[2])

    def messageTestA(self, _testdata_):
        testdata_ = _testdata_
        testdata = testdata_.copy()
        testdata.pop('articleBody_html')
        testdata.pop('hashtags')
        testdata.pop('usertags')
        u = self.create_testdata_user(testdata)

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

        User = get_user_model()
        _users = []
        for username in testdata_['usertags']:
            _user = User.objects.get(username=username)
            _users.append(_user)
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

    def test_new_notloggedin(self):
        c = Client()
        resp = c.get('/new', follow=True)
        self.assertEqual('/accounts/login/?next=/new',
                         resp.redirect_chain[0][0])

    def test_new(self):
        testdata = LINKIFY_TESTDATA[1].copy()
        testdata['password'] = 'password'
        User = get_user_model()
        user = User(username=testdata['user'])
        user.set_password(testdata['password'])
        user.save()

        c = Client()
        c.login(username=user.username, password=testdata['password'])
        resp = c.get('/new')
        self.assertContains(resp, '''<input type="submit" value="Post" />''')

        resp = c.post('/new', data=dict(articleBody=testdata['articleBody']),
                      follow=True)
        self.assertContains(resp, testdata['articleBody_html'])


class TestAppconfig(unittest.TestCase):
    def test_appconfig(self):
        from djangotestapp.testapp.apps import TestappConfig
        self.assertEqual(TestappConfig.name, 'testapp')


import pprint
from rest_framework.test import APITestCase


class JSONAPITestCase(APITestCase):
    def assertJSONLenAndEqual(self, resp1, resp2):
        try:
            resp1_json = resp1.json()
        except ValueError as e:
            output = repr(resp1.__dict__)
            e.args = (u"%s\n%s" % (e.args[0], output),)
            raise
        try:
            resp2_json = resp2.json()
        except ValueError as e:
            output = repr(resp2.__dict__)
            e.args = (u"%s\n%s" % (e.args[0], output),)
            raise
        self.assertTrue(len(resp2.json()))
        self.assertTrue(len(resp1.json()))
        try:
            self.assertEqual(resp1_json, resp2_json)
        except AssertionError as e:
            import json
            str1 = json.dumps(resp1_json, indent=2)
            str2 = json.dumps(resp2_json, indent=2)
            import difflib
            output = u'\n'.join(
                difflib.unified_diff(str1.splitlines(), str2.splitlines()))
            e.args = (u"%s\n%s" % (e.args[0], output),)
            raise
        return resp1_json, resp2_json


class APITestCase_(JSONAPITestCase):
    fixtures = ['djangotestapp/fixtures/dump.json']

    longMessage = True

    def debug_response(self, resp):
        output = []
        output.append(pprint.pformat(resp.__dict__))
        req = resp.renderer_context['request'].__dict__
        output.append(pprint.pformat(req))
        output.append(pprint.pformat(req['_user']))
        return u'\n'.join(output)

    def assertHTTPCode(self, code, resp):
        # 200 OK
        # 201 Added
        # 401 Unauthorized
        # 405 Method not Allowed
        try:
            self.assertEqual(resp.status_code, code)
        except AssertionError as e:
            e.args = (u"%s\n%s" % (e.args[0], self.debug_response(resp)),)
            raise

    def loginAsAdmin(self):
        # DEFAULT_PASSWORD = 'password'
        # self.admin.set_password(DEFAULT_PASSWORD)
        # self.client.login(username=self.admin.username,
        #                   password=DEFAULT_PASSWORD)
        self.client.force_authenticate(user=self.admin)

    def setUp(self):
        self.User = get_user_model()
        DEFAULT_ADMIN_USERNAME = 'admin'
        self.admin = self.User.objects.get(
            username=DEFAULT_ADMIN_USERNAME)
        if hasattr(self, 'setUp_'):
            self.setUp_()
        return super(APITestCase, self).setUp()


class TestAPITestCase_(APITestCase_): #
    def test_asserts_fail(self):
        c = self.client
        resp1 = c.get(reverse('message-list', kwargs=dict(format='json')))
        resp2 = c.get(reverse('message-detail', kwargs=dict(pk=1, format='json')))
        with self.assertRaises(AssertionError):
            self.assertJSONLenAndEqual(resp1, resp2)
        with self.assertRaises(AssertionError):
            self.assertHTTPCode(201, resp1)
        resp3 = c.get('/@admin')
        with self.assertRaises(ValueError):
            self.assertJSONLenAndEqual(resp1, resp3)
        with self.assertRaises(ValueError):
            self.assertJSONLenAndEqual(resp3, resp1)


class TestAPI_Messages(APITestCase_):

    def setUp_(self):
        self.testdata = {
            'articleBody': 'example #message @user',
            'user': self.admin.username}

    def test_messages_get(self):
        c = self.client
        resp1 = c.get(reverse('message-list'))
        resp2 = c.get('/api/v1/messages/')
        self.assertJSONLenAndEqual(resp1, resp2)

        resp1 = c.get(reverse('message-detail', kwargs=dict(
            pk=1, format='json')))
        resp2 = c.get('/api/v1/messages/1.json')
        self.assertJSONLenAndEqual(resp1, resp2)

    def test_messages_post_unauthorized(self):
        c = self.client
        testdata = self.testdata
        resp1 = c.post(reverse('message-list'), testdata)
        self.assertHTTPCode(401, resp1)

    def test_messages_post_0(self):
        c = self.client
        testdata = self.testdata
        self.loginAsAdmin()
        resp1 = c.post(reverse('message-list', kwargs=dict(format='json')), testdata)
        resp2 = c.post('/api/v1/messages.json', testdata)
        self.assertHTTPCode(405, resp1)
        self.assertHTTPCode(405, resp2)


class TestAPI_MyMessages(APITestCase_): # TODO

    def setUp_(self):
        self.testdata = {
            'articleBody': 'example #mymessage @user',
            'user': self.admin.username}

    def test_mymessages_get(self):
        c = self.client
        self.loginAsAdmin()
        resp1 = c.get(reverse('mymessage-list'))
        resp2 = c.get('/api/v1/mymessages/')
        self.assertJSONLenAndEqual(resp1, resp2)

        resp1 = c.get(reverse('mymessage-detail', kwargs=dict(
            pk=1, format='json')))
        resp2 = c.get('/api/v1/mymessages/1.json')
        self.assertJSONLenAndEqual(resp1, resp2)

    def test_mymessages_post_unauthorized(self):
        c = self.client
        testdata = self.testdata
        resp1 = c.post(reverse('mymessage-list'), testdata)
        self.assertHTTPCode(401, resp1)

    def test_mymessages_post_0(self):
        c = self.client
        testdata = self.testdata
        self.loginAsAdmin()
        resp1 = c.post(reverse('mymessage-list', kwargs=dict(format='json')), testdata)
        resp2 = c.post('/api/v1/mymessages.json', testdata)
        self.assertHTTPCode(201, resp1)
        self.assertHTTPCode(201, resp2)

        id1 = resp1.json()['id']
        resp11 = c.get(reverse('mymessage-detail', kwargs=dict(pk=id1, format='json')))
        self.assertHTTPCode(200, resp11)
        self.assertJSONLenAndEqual(resp1, resp11)
        id2 = resp2.json()['id']
        resp22 = c.get(reverse('mymessage-detail', kwargs=dict(pk=id2, format='json')))
        self.assertHTTPCode(200, resp22)
        self.assertJSONLenAndEqual(resp2, resp22)


class TestAPI_Hashtags(APITestCase_):

    def setUp_(self):
        self.testdata = {'name': 'testtest'}

    def test_hashtags_get(self):
        c = self.client
        resp1 = c.get(reverse('hashtag-list'))
        resp2 = c.get('/api/v1/hashtags/')
        self.assertJSONLenAndEqual(resp1, resp2)

        resp1 = c.get(reverse('hashtag-detail', kwargs=dict(name='hashtag', format='json')))
        resp2 = c.get('/api/v1/hashtags/hashtag.json')
        self.assertJSONLenAndEqual(resp1, resp2)

    def test_hashtags_post_unauthorized(self):
        c = self.client
        testdata = self.testdata
        resp1 = c.post(reverse('hashtag-list'), testdata)
        self.assertHTTPCode(401, resp1)

    def test_hashtags_post_0__readonly(self):
        c = self.client
        testdata = self.testdata
        self.loginAsAdmin()
        resp1 = c.post(reverse('hashtag-list'), testdata)
        self.assertHTTPCode(405, resp1)


class TestAPI_Users(APITestCase_):

    def setUp_(self):
        self.testdata = {'username': 'testusername', }

    def test_users_get(self):
        c = self.client
        resp1 = c.get(reverse('user-list'))
        resp2 = c.get('/api/v1/users/')
        self.assertJSONLenAndEqual(resp1, resp2)

        resp1 = c.get(reverse('user-detail', kwargs=dict(pk=1, format='json')))
        resp2 = c.get('/api/v1/users/1.json')
        self.assertJSONLenAndEqual(resp1, resp2)

    def test_users_post_unauthorized(self):
        c = self.client
        testdata = self.testdata
        resp1 = c.post(reverse('user-list'), testdata)
        self.assertHTTPCode(401, resp1)

    def test_users_post_0__readonly(self):
        c = self.client
        testdata = self.testdata
        self.loginAsAdmin()
        resp1 = c.post(reverse('user-list'), testdata)
        self.assertHTTPCode(405, resp1)
