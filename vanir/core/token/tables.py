from vanir.utils.tables import ObjectTable

from .models import Token


class TokenTable(ObjectTable):
    def render_last_value(self, value):
        if value == 0:
            return "Pair not supported"
        else:
            return value

    class Meta:
        model = Token
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "symbol", "last_value")
