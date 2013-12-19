from django.utils import timezone
from django.test import TestCase
from linter.models import Clipping
from django.core.exceptions import ValidationError
from datetime import datetime


class Validation_Tests(TestCase):

    # python manage.py dumpdata --indent=4 > newslint/fixtures/projects.json & then remove system objects

    def setUp(self):

        Clipping.objects.create(
            title='test clipping',
            url='http://google.com/',
            publication='False Publication',
            content='test content'
        )

        Clipping.objects.create(
            title='test clipping 2',
            url='http://google.com/',
            publication='FOX News',
            content='test content',
            added=timezone.now()
        )

    def test_projects(self):
        clipping_1 = Clipping.objects.get(title='test clipping')
        clipping_2 = Clipping.objects.get(title='test clipping 2')
        with self.assertRaises(ValidationError):
            clipping_1.clean_fields()
        self.assertEqual(clipping_2.clean_fields(), None)


class Server_Route_Tests(TestCase):

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_clippings(self):
        resp = self.client.get('/clippings/')
        self.assertEqual(resp.status_code, 200)

    def test_lint(self):
        resp = self.client.get('/lint/')
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        resp = self.client.post('/post/', {'content': "chris%20hayes"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(1.0, resp.context['result']['total'])
        self.assertTrue(1.0, resp.context['result']['credibility'])
        self.assertTrue("chris%20hayes", resp.context['content'])

    def test_clipping(self):
        resp = self.client.get('/clipping/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('total' in resp.context['result'])

    def test_about(self):
        resp = self.client.get('/about/')
        self.assertEqual(resp.status_code, 200)


class API_Route_Tests(TestCase):

    api_prefix = '/api/v1/'

    def test_api_index(self):
        resp = self.client.get(self.api_prefix)
        self.assertEqual(resp.status_code, 200)

    def test_api_list(self):
        resp = self.client.get(self.api_prefix + 'clippings/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('"clippings_list":' in resp.content)

    def test_api_clipping(self):
        resp = self.client.get(self.api_prefix + 'clipping/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('"total":' in resp.content)

    def test_api_linter(self):
        resp = self.client.get(self.api_prefix + 'linter/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('"total":' in resp.content)

    def test_api_linter_get(self):
        resp = self.client.get(self.api_prefix + 'linter/?content=test')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('"content": "test"' in resp.content)

    def test_api_linter_post(self):
        resp = self.client.post(self.api_prefix + 'linter/', {'content': "chris%20hayes"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('"content": "chris%20hayes"' in resp.content)
        self.assertTrue('"credibility": 1.0' in resp.content)
        self.assertTrue('"total": 1.0' in resp.content)

    def test_api_help(self):
        resp = self.client.get(self.api_prefix + 'help/')
        self.assertEqual(resp.status_code, 200)


class DB_Tests(TestCase):

    api_prefix = '/api/v1/'

    def test_post_simple(self):
        resp = self.client.post("/post/", {"content": "obamacare", "publication": "The Blaze", "author": "bill o'reilly"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.templates) > 0)

    def test_post_public(self):
        resp = self.client.post("/post/", {"content": "chris hayes", "publication": "The Blaze", "author": "test author", "public": "on"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.templates) > 0)
        self.assertTrue('permanent URL' in resp.content)

    def test_post_public_with_published_date(self):
        resp = self.client.post("/post/", {"content": "chris hayes", "publication": "The Blaze", "author": "test author2", "public": "on", "published": "11/11/13"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.templates) > 0)
        self.assertTrue('permanent URL' in resp.content)

        # now fetch it from db
        test_clipping = Clipping.objects.get(author="test author2")
        self.assertEqual('11/11/13', test_clipping.published.strftime('%m/%d/%y'))
        resp = self.client.get('/clipping/' + str(test_clipping.id))
        self.assertEqual(resp.status_code, 200)

    def test_api_post_public_with_published_date(self):
        resp = self.client.post("/api/v1/post/", {"content": "chris hayes", "publication": "The Blaze", "author": "test author3", "public": "on", "published": "11/12/13"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('"content": "chris hayes"' in resp.content)

        # now fetch it from db
        test_clipping2 = Clipping.objects.get(author="test author3")
        self.assertEqual('11/12/13', test_clipping2.published.strftime('%m/%d/%y'))
        resp = self.client.get('/clipping/' + str(test_clipping2.id))
        self.assertEqual(resp.status_code, 200)
