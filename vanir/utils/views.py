from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django_tables2 import SingleTableView

from vanir.utils.forms import PopulateDBBinanceForm


@method_decorator(login_required, name="dispatch")
class ObjectCreateView(CreateView):
    model = None
    template_name = "object_form.html"


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


class PopulateDBBinanceView(FormView):
    form_class = PopulateDBBinanceForm
    template_name = "basic_form.html"
    success_url = reverse_lazy("token:token_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Populate DB with Binance"
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.populate_db()
        return super().form_valid(form)
