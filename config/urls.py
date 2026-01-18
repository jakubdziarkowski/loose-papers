from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("admin/", admin.site.urls),
    path("api/accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
]
