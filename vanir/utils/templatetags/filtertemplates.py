import json
import os

from django import template
from django.conf import settings
from django.templatetags.static import static as templatetags_static
from django.urls import NoReverseMatch, reverse

from vanir.utils.helpers import fetch_default_account

register = template.Library()


@register.filter
def add_class(field, class_name):
    return field.as_widget(attrs={"class": " ".join((field.css_classes(), class_name))})


@register.filter
def pretty_json(value):
    return json.dumps(value, indent=4)


@register.filter()
def validated_viewname(model, action):
    """
    Return the view name for the given model and action if valid, or None if invalid.
    """
    viewname = f"{model._meta.app_label}:{model._meta.model_name}_{action}"
    try:
        # Validate and return the view name. We don't return the actual URL yet because many of the templates
        # are written to pass a name to {% url %}.
        if action in ("balance_import", "edit", "more", "update", "delete"):
            reverse(viewname, kwargs={"pk": model.pk})
        else:
            reverse(viewname)
        return viewname
    except NoReverseMatch:
        return None


@register.filter()
def get_viewname(model_name: str, action: str):
    viewname = f"{model_name.lower()}:{model_name.lower()}_{action}"
    try:
        # Validate and return the view name. We don't return the actual URL yet because many of the templates
        # are written to pass a name to {% url %}.
        reverse(viewname)
        return viewname
    except NoReverseMatch:
        return None


@register.filter()
def get_model_image(model_name, image_name: str = ""):
    path_name = (
        f"images/{model_name}/{model_name}.png"
        if not image_name
        else f"images/{model_name}/{image_name}"
    )
    if settings.DEBUG:
        if os.path.exists(f"{settings.APPS_DIR}{templatetags_static(path_name)}"):
            return path_name
        else:
            return None
    return path_name


@register.filter()
def get_model_name(model):
    return model._meta.model_name


@register.filter()
def account_token_value(account, token_name):
    for tokenqty in account.accounttokens_set.all():
        if tokenqty.token.name == token_name:
            try:
                return round(tokenqty.token.last_value * tokenqty.quantity, 2)
            except TypeError:
                return tokenqty.quantity


@register.simple_tag
def default_pair_symbol():
    return fetch_default_account().token_pair
