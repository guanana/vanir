import django_tables2 as tables


class ObjectTable(tables.Table):
    name = tables.TemplateColumn('<a href="{{record.get_absolute_url}}edit/">{{record.name}}</a>')

    class Meta:
        model = None
        template_name = "django_tables2/bootstrap.html"

