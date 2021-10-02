from vanir.utils.views import ObjectListView, set_context_data


class PluginListView(ObjectListView):
    model = None
    table_class = None
    template_name = "object_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = True
        context["title"] = f" plugin {context['model_name']}"
        return set_context_data(context, self)
