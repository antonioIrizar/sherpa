import logging
from typing import Optional

import requests

from . import settings

logger = logging.getLogger(__name__)


def get_city_by_postcode(postcode: str) -> Optional[str]:
    params = {
        "country": settings.GEONAMES_COUNTRY,
        "postalcode": postcode,
        "username": settings.GEONAMES_USERNAME,
    }

    try:
        response = requests.get(settings.GEONAMES_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        logger.exception("Error to get city from post code service")
        return None

    postal_codes = response.json().get("postalCodes", [])
    if len(postal_codes) > 1:
        raise ValueError("multiples cities for same postcode")
    if not postal_codes:
        return None
    return postal_codes[0]["placeName"]
