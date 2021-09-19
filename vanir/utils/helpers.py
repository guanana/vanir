from django.apps import apps
from django.conf import settings


def get_nav_menu(context):
    context["apps"] = {}
    user_installed_apps = settings.LOCAL_APPS
    list_apps = [user_apps.split('.')[1] for user_apps in user_installed_apps]
    for app in apps.all_models:
        if app in list_apps and not (app == "users" or app == "utils"):
            context["apps"].update({app.capitalize(): {"list": f"{app}:{app}_list", "add": f"{app}:{app}_add"}})
    return context
