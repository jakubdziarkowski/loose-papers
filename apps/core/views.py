from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def mock_ui(request: HttpRequest) -> HttpResponse:
    return render(request, "core/mock_ui.html")
