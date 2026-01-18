from django.urls import path

from .views import mock_ui

urlpatterns = [
    path("", mock_ui, name="mock-ui"),
]
