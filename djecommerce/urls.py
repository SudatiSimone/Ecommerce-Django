from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls",)),
    path("", include("core.urls", namespace="core")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    SHOW_TOOLBAR_CALLBACK = True


if settings.DEBUG:
    import debug_toolbar
