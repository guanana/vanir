from django.apps import apps
from django.conf import settings


def get_nav_menu(context):
    context["apps"] = {}
    user_installed_apps = settings.LOCAL_APPS
    list_apps = [user_apps.split(".")[1] for user_apps in user_installed_apps]
    for app in apps.all_models:
        if app in list_apps and not (app == "users" or app == "utils"):
            context["apps"].update(
                {
                    app.capitalize(): {
                        "list": f"{app}:{app}_list",
                        "add": f"{app}:{app}_add",
                    }
                }
            )
    return context


def change_table_style(table_html, html_class="text-center thead-light"):
    return table_html.replace("<thead>", f"<thead class='{html_class}>'")


def change_table_align(table_html, align="center"):
    return table_html.replace("text-align: right;", f"text-align: {align};")
