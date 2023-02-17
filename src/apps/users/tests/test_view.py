import requests_mock
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from . import fixture
from .. import models
from .. import settings


@requests_mock.Mocker()
class UserViewTest(TestCase):
    def test_create_user(self, m):
        m.get(settings.GEONAMES_URL, json=fixture.VALID_RESPONSE_GEONAMES)
        client = Client()
        response = client.post(
            reverse("users:users"), {"postcode": "12345", "username": "test@test.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            models.Master.objects.filter(username="test@test.com").count(), 1
        )
        self.assertEqual(
            models.Detail.objects.filter(master_set__username="test@test.com").count(),
            1,
        )
