from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django_tables2 import SingleTableView


@method_decorator(login_required, name="dispatch")
class ObjectCreateView(CreateView):
    model = None
    template_name = "object_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model.__name__
        return context


@method_decorator(login_required, name="dispatch")
class ObjectListView(SingleTableView):
    model = None
    table_class = None
    template_name = "object_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.model.__name__.lower()
        context["model_name"] = model_name
        context["model_url"] = f"{model_name}:{model_name}_add"
        return context


@method_decorator(login_required, name="dispatch")
class ObjectUpdateView(UpdateView):
    model = None
    fields = "__all__"
    template_name = "object_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model.__name__.lower()
        return context


@method_decorator(login_required, name="dispatch")
class ObjectDetailView(DetailView):
    model = None


@method_decorator(login_required, name="dispatch")
class ObjectDeleteView(DeleteView):
    model = None
    template_name = "object_delete_confirm.html"
    success_url = "/"


class HomeView(TemplateView):
    template_name = "pages/home.html"
