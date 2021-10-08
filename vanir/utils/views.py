from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin

from vanir.utils.forms import PopulateDBBinanceForm


def set_context_data(context, view):
    app_label = view.model._meta.app_label
    model_name = view.model._meta.model_name
    context["app_label"] = app_label
    context["model_name"] = model_name
    context["title"] = model_name.capitalize()
    return context


class ObjectCreateView(LoginRequiredMixin, CreateView):
    model = None
    template_name = "object_form.html"


class ObjectListView(LoginRequiredMixin, SingleTableView):
    model = None
    table_class = None
    template_name = "object_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return set_context_data(context, self)


class ObjectListFilterView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = None
    table_class = None
    filterset_class = None
    template_name = "object_list.html"
    table_pagination = {"per_page": 15}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return set_context_data(context, self)


class ObjectUpdateView(LoginRequiredMixin, UpdateView):
    model = None
    fields = "__all__"
    template_name = "object_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_button"] = "Apply"
        return set_context_data(context, self)


class ObjectDetailView(DetailView):
    model = None
    table_class = None
    template_name = "object_detail.html"

    def get_context_data(self, **kwargs):
        table = self.table_class(self.model.objects.filter(pk=self.kwargs["pk"]))
        context = {"table": table}
        return super().get_context_data(**context)


# TODO: Check how to pass into table
# class ObjectDetailView(LoginRequiredMixin, SingleTableView):
#     model = None


class ObjectDeleteView(LoginRequiredMixin, DeleteView):
    model = None
    template_name = "object_delete_confirm.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return set_context_data(context, self)


class HomeView(TemplateView):
    template_name = "pages/home.html"


class PopulateDBBinanceView(SuccessMessageMixin, FormView):
    form_class = PopulateDBBinanceForm
    template_name = "basic_form.html"
    success_url = reverse_lazy("token:token_list")
    success_message = "Import completed"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Populate DB with Binance"
        context["form_button"] = "Apply"
        return context

    def post(self, request, *args: str, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.populate_db()
        return super().form_valid(form)
