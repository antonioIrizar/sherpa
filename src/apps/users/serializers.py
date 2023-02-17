from django.db import transaction
from rest_framework import serializers

from . import models
from . import utils


class MasterSerializer(serializers.ModelSerializer):
    postcode = serializers.CharField(source="detail.postcode")
    city = serializers.CharField(source="detail.city", read_only=True)
    _city = None

    def validate_postcode(self, value: str) -> str:
        try:
            self._city = utils.get_city_by_postcode(value)
        except ValueError:
            raise serializers.ValidationError("multiples cities for same postcode")
        if not self._city:
            raise serializers.ValidationError("Invalid postcode")
        return value

    @transaction.atomic
    def create(self, validated_data: dict) -> models.Master:
        detail, _ = models.Detail.objects.get_or_create(
            postcode=validated_data["detail"]["postcode"], city=self._city
        )
        return models.Master.objects.create(
            username=validated_data["username"], detail=detail
        )

    class Meta:
        fields = ("username", "postcode", "city")
        model = models.Master
