from django.db import models


class BaseObject(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def get_absolute_url(self):
        from django.urls import reverse

        class_name = self.__class__.__name__.lower()
        return reverse(f"{class_name}:{class_name}_detail", kwargs={"pk": self.pk})

    def get_add_url(self):
        from django.urls import reverse

        class_name = self.__name__.lower()
        return reverse(f"{class_name}:{class_name}_add")


class TimeStampedMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
