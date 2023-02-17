import requests
import requests_mock
from django.test import TestCase

from . import fixture
from .. import settings
from .. import utils


@requests_mock.Mocker()
class UtilsTest(TestCase):
    def test_get_city_by_postcode(self, m):
        m.get(settings.GEONAMES_URL, json=fixture.VALID_RESPONSE_GEONAMES)

        self.assertEqual(
            utils.get_city_by_postcode("12345"),
            fixture.VALID_RESPONSE_GEONAMES["postalCodes"][0]["placeName"],
        )

    def test_get_city_by_postcode_request_exception(self, m):
        m.get(settings.GEONAMES_URL, exc=requests.exceptions.RequestException)
        self.assertIsNone(utils.get_city_by_postcode("12345"))

    def test_get_city_by_postcode_not_found_code(self, m):
        m.get(settings.GEONAMES_URL, json=fixture.NOT_FOUND_RESPONSE_GEONAMES)
        self.assertIsNone(utils.get_city_by_postcode("12345"))

    def test_get_city_by_postcode_multiple_cities(self, m):
        m.get(settings.GEONAMES_URL, json=fixture.MULTIPLE_CITIES_RESPONSE_GEONAMES)
        with self.assertRaisesMessage(ValueError, "multiples cities for same postcode"):
            utils.get_city_by_postcode("12345")
