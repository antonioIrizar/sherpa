import uuid
from django.db import models
from model_utils.models import TimeStampedModel


class AbstractTimeStampedUUID(TimeStampedModel):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Detail(TimeStampedModel):
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=128)

    class Meta:
        unique_together = (
            "postcode",
            "city",
        )


class Master(AbstractTimeStampedUUID):
    username = models.EmailField(db_index=True, unique=True)
    detail = models.ForeignKey(
        Detail, on_delete=models.CASCADE, related_name="master_set"
    )
