from unittest import mock

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .. import factories
from .. import models
from .. import serializers


class MasterSerializerTest(TestCase):
    @property
    def data(self) -> dict:
        return {"postcode": "12345", "username": "test@test.com"}

    def test_valid(self):
        serializer = serializers.MasterSerializer(data=self.data)

        with mock.patch("users.utils.get_city_by_postcode", return_value="city"):
            self.assertTrue(serializer.is_valid())
            self.assertEqual(serializer._city, "city")

    def test_not_city(self):
        serializer = serializers.MasterSerializer(data=self.data)

        with mock.patch(
            "users.utils.get_city_by_postcode", return_value=None
        ), self.assertRaisesMessage(
            ValidationError,
            "{'postcode': [ErrorDetail(string='Invalid postcode', code='invalid')]}",
        ):
            serializer.is_valid(raise_exception=True)

    def test_multiple_cities(self):
        serializer = serializers.MasterSerializer(data=self.data)
        with mock.patch(
            "users.utils.get_city_by_postcode", side_effect=ValueError
        ), self.assertRaisesMessage(
            ValidationError,
            "{'postcode': [ErrorDetail(string='multiples cities for same postcode', code='invalid')]}",
        ):
            serializer.is_valid(raise_exception=True)

    def test_save(
        self,
    ):
        serializer = serializers.MasterSerializer(data=self.data)
        with mock.patch("users.utils.get_city_by_postcode", return_value="city"):
            serializer.is_valid()

        serializer.save()

        master = models.Master.objects.get(username="test@test.com")

        self.assertEqual(master.detail.postcode, "12345")

    def test_already_exists_users(self):
        factories.MasterFactory(username="test@test.com")
        serializer = serializers.MasterSerializer(data=self.data)

        with mock.patch(
            "users.utils.get_city_by_postcode", return_value="city"
        ), self.assertRaisesMessage(
            ValidationError,
            "{'username': [ErrorDetail(string='master with this username already exists.', code='unique')]}",
        ):
            serializer.is_valid(raise_exception=True)

    def test_save_already_exist_detail(self):
        factories.DetailFactory(postcode="12345", city="city")
        serializer = serializers.MasterSerializer(data=self.data)

        with mock.patch("users.utils.get_city_by_postcode", return_value="city"):
            serializer.is_valid()
        serializer.save()

        self.assertEqual(models.Detail.objects.count(), 1)
