from django.db import models


class Blockchain(models.Model):
    name = models.CharField(max_length=100)
    project_url = models.URLField()
    explorer_url = models.URLField()

    def __str__(self):
        return self.name

