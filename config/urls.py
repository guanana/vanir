from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from rest_framework.authtoken.views import obtain_auth_token

from vanir.utils.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("vanir.users.urls", namespace="users")),
    path("account/", include("vanir.account.urls", namespace="account")),
    path("exchange/", include("vanir.exchange.urls", namespace="exchange")),
    path("blockchain/", include("vanir.blockchain.urls", namespace="blockchain")),
    path("token/", include("vanir.token.urls", namespace="token")),
    path("order/", include("vanir.order.urls", namespace="order")),
    path("utils/", include("vanir.utils.urls", namespace="utils")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
