from django.db import models

from vanir.utils.models import BaseObject


class PluginBase(BaseObject):
    name = models.CharField(max_length=250)

    class Meta:
        abstract = True
        app_label = "plugins"
