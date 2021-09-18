import django_tables2 as tables
from .models import Blockchain


class BlockchainTable(tables.Table):
    class Meta:
        model = Blockchain
        template_name = "django_tables2/bootstrap.html"
