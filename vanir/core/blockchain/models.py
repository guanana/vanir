from django.db import models

from vanir.utils.models import BaseObject


class Blockchain(BaseObject):
    project_url = models.URLField()
    explorer_url = models.URLField()
