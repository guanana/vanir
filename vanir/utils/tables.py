import django_tables2 as tables


class ObjectTable(tables.Table):
    name = tables.Column(linkify=True)

    class Meta:
        model = None
        template_name = "django_tables2/bootstrap.html"
