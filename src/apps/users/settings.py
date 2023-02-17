import os


GEONAMES_URL = "http://api.geonames.org/postalCodeSearchJSON"
GEONAMES_COUNTRY = os.getenv("GEONAMES_COUNTRY", "ES")
GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")
