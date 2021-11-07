from django.http import HttpResponse
from django.template import loader


def exchange_view_render(
    template_name: str, response, request, **kwargs
) -> HttpResponse:
    """
    Helper for extra views in account
    :param template_name: Template name to render
    :type template_name: str
    :param response: View parameter
    :param request: View parameter
    :param kwargs: View parameter
    :return: HTTP render view
    :rtype: HttpResponse
    """
    template = loader.get_template(template_name)
    context = {"con": response, **kwargs}
    return HttpResponse(template.render(context, request))
