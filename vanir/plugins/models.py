from vanir.utils.models import BaseObject


class PluginBase(BaseObject):
    class Meta:
        abstract = True

    def get_absolute_url(self):
        from django.urls import reverse

        app_label = self._meta.app_label
        model_name = self._meta.model_name
        return reverse(
            f"plugins:{app_label}:{model_name}_detail", kwargs={"pk": self.pk}
        )

    @property
    def get_list_url(self):
        from django.urls import reverse

        app_label = self._meta.app_label
        class_name = self.__class__.__name__.lower()
        return reverse(f"plugins:{app_label}:{class_name}_list")

    @property
    def get_add_url(self):
        from django.urls import reverse

        app_label = self._meta.app_label
        model_name = self._meta.model_name
        return reverse(f"plugins:{app_label}:{model_name}_add")
