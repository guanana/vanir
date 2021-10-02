from vanir.utils.models import BaseObject


class PluginBase(BaseObject):
    class Meta:
        abstract = True
        app_label = "plugins"

    def get_absolute_url(self):
        from django.urls import reverse

        class_name = self.__class__.__name__.lower()
        return reverse(
            f"plugins:{class_name}:{class_name}_detail", kwargs={"pk": self.pk}
        )
