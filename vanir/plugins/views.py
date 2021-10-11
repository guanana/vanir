from vanir.utils.templatetags.filtertemplates import get_display_name
from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListFilterView,
    ObjectListView,
    ObjectUpdateView,
    set_context_data,
)


class PluginCreateView(ObjectCreateView):
    model = None
    template_name = "object_form.html"


class PluginListView(ObjectListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = True
        context["title"] = f"Plugin {get_display_name(self.model)}"
        return set_context_data(context, self)


class PluginListFilterView(ObjectListFilterView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = True
        context["title"] = f"Plugin {get_display_name(self.model)}"
        return set_context_data(context, self)


class PluginUpdateView(ObjectUpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = True
        context["title"] = f"Plugin {get_display_name(self.model)}"
        return set_context_data(context, self)


class PluginDetailView(ObjectDetailView):
    model = None
    template_name = "object_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = True
        return set_context_data(context, self)


class PluginDeleteView(ObjectDeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = True
        context["title"] = f"Plugin {get_display_name(self.model)}"
        return set_context_data(context, self)
