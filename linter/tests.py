from django.utils import timezone
from django.test import TestCase
from linter.models import Clipping
from django.core.exceptions import ValidationError


class Validation_Tests(TestCase):

    fixtures = ['projects.json']  # python manage.py dumpdata --indent=4 > newslint/fixtures/projects.json

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

    fixtures = ['clippings.json']

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_clippings(self):
        resp = self.client.get('/clippings/')
        self.assertEqual(resp.status_code, 200)


class API_Route_Tests(TestCase):

    fixtures = ['clippings.json']
    api_prefix = '/api/v1/'

    def test_api_index(self):
        resp = self.client.get(self.api_prefix)
        self.assertEqual(resp.status_code, 200)

    def test_api_linter(self):
        resp = self.client.get(self.api_prefix + 'linter/')
        self.assertEqual(resp.status_code, 200)
