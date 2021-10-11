import json

from django import template
from django.urls import NoReverseMatch, reverse

from vanir.utils.helpers import fetch_default_account

register = template.Library()


@register.filter
def add_class(field, class_name):
    return field.as_widget(attrs={"class": " ".join((field.css_classes(), class_name))})


@register.filter
def pretty_json(value):
    return json.dumps(value, indent=4)


def _try_validated_plugin(model, action):
    try:
        viewname = f"plugins:{model._meta.app_label}:{model._meta.model_name}_{action}"
        reverse(viewname)
        return viewname
    except NoReverseMatch:
        try:
            reverse(viewname, kwargs={"pk": model.pk})
            return viewname
        except NoReverseMatch:
            return None


@register.filter()
def validated_viewname(model, action):
    """
    Return the view name for the given model and action if valid, or None if invalid.
    """
    try:
        viewname = f"{model._meta.app_label}:{model._meta.model_name}_{action}"
    except AttributeError:
        return model
    try:
        # Validate and return the view name. We don't return the actual URL yet because many of the templates
        # are written to pass a name to {% url %}.
        reverse(viewname)
        return viewname
    except NoReverseMatch:
        try:
            reverse(viewname, kwargs={"pk": model.pk})
            return viewname
        except NoReverseMatch:
            viewname = _try_validated_plugin(model, action)
            if viewname:
                return viewname
            return "Validated View name ERROR"


@register.filter()
def get_model_image(model_name, image_name: str = ""):
    path_name = (
        f"images/{model_name}/{model_name}.png"
        if not image_name
        else f"images/{model_name}/{image_name}"
    )
    return path_name


@register.filter()
def get_model_name(model):
    if model == "":
        return "Custom"
    return model._meta.model_name


@register.filter()
def get_display_name(model):
    try:
        return model.get_title()
    except AttributeError:
        return model._meta.model_name.capitalize()


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
    account = fetch_default_account()
    if not account:
        return ""
    return fetch_default_account().token_pair


@register.simple_tag
def get_viewname(app_label: str, model_name: str, action: str, plugin: bool = False):
    if plugin:
        viewname = f"plugins:{app_label.lower()}:{model_name.lower()}_{action}"
    else:
        viewname = f"{app_label.lower()}:{model_name.lower()}_{action}"
    try:
        # Validate and return the view name. We don't return the actual URL yet because many of the templates
        # are written to pass a name to {% url %}.
        return reverse(viewname)
    except NoReverseMatch:
        return None
