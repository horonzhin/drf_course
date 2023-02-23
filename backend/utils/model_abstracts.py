import uuid
from django.db import models


class Model(models.Model):
    """
    A custom abstract class that uses UUID instead of the default ID field.
    Then we use this class in our contact model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True
