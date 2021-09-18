from .models import Blockchain
from vanir.utils.tables import ObjectTable


class BlockchainTable(ObjectTable):
    class Meta:
        model = Blockchain
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "project_url", "explorer_url")
