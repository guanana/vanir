from django import template
from django.core.exceptions import ValidationError
from django.urls import reverse

from vanir.utils.templatetags.filtertemplates import validated_viewname

register = template.Library()


def _validated_viewname_by_context(context, action):
    if not context or not action:
        raise ValidationError("Something went wrong with viewname validation")
    viewname = f'{context["app_label"]}:{context["model_name"]}_{action}'
    try:
        if context["plugin"]:
            viewname = (
                f'plugins:{context["app_label"]}:{context["model_name"]}_{action}'
            )
    except KeyError:
        pass
    return viewname


@register.inclusion_tag("buttons/edit.html")
def edit_button(instance):
    viewname = validated_viewname(instance, "edit")
    url = reverse(viewname, kwargs={"pk": instance.pk})

    return {
        "url": url,
    }


@register.inclusion_tag("buttons/delete.html")
def delete_button(instance):
    viewname = validated_viewname(instance, "delete")
    url = reverse(viewname, kwargs={"pk": instance.pk})

    return {
        "url": url,
    }


@register.inclusion_tag("buttons/cancel_order.html")
def cancel_order_button(instance):
    viewname = validated_viewname(instance, "delete")
    url = reverse(viewname, kwargs={"pk": instance.pk})

    return {
        "url": url,
    }


#
# List buttons
#


@register.inclusion_tag("buttons/add.html", takes_context=True)
def add_button(context):
    viewname = _validated_viewname_by_context(context, "add")
    url = reverse(viewname)

    return {
        "add_url": url,
    }


#
# Detail buttons
#


@register.inclusion_tag("buttons/back.html")
def back_button(instance):
    return {
        "back_url": instance.get_list_url,
    }
