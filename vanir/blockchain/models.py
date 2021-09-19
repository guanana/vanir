from django.db import models

from vanir.utils.models import BaseObject


class Blockchain(BaseObject):
    name = models.CharField(max_length=100)
    project_url = models.URLField()
    explorer_url = models.URLField()
