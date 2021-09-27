from vanir.utils.tables import ObjectTable

from .models import Blockchain


class BlockchainTable(ObjectTable):
    class Meta:
        model = Blockchain
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "project_url", "explorer_url")
