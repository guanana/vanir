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
