from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase


class RootUrl(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_root_url(self):
        response = self.client.get(reverse('api_root'))
        self.assertEqual(response.status_code, 200)
