import factory
from . import models


class DetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Detail


class MasterFactory(factory.django.DjangoModelFactory):
    detail = factory.SubFactory(DetailFactory)

    class Meta:
        model = models.Master
