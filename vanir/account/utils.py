from django.http import HttpResponse
from django.template import loader


def exchange_view_render(template_name, response, request, **kwargs):
    template = loader.get_template(template_name)
    context = {"con": response, **kwargs}
    return HttpResponse(template.render(context, request))
