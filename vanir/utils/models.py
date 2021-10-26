from django.db import models


class BaseObject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def get_absolute_url(self):
        from django.urls import reverse

        app_label = self._meta.app_label
        class_name = self.__class__.__name__.lower()
        return reverse(f"{app_label}:{class_name}_detail", kwargs={"pk": self.pk})

    @property
    def get_list_url(self):
        from django.urls import reverse

        app_label = self._meta.app_label
        class_name = self.__class__.__name__.lower()
        return reverse(f"{app_label}:{class_name}_list")

    @property
    def get_add_url(self):
        from django.urls import reverse

        app_label = self._meta.app_label
        model_name = self._meta.model_name
        return reverse(f"{app_label}:{model_name}_add")


class TimeStampedMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
