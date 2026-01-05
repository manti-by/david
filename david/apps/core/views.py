from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from david.apps.core.tasks import debug_logger


def index_view(request: HttpRequest) -> HttpResponse:
    debug_logger.delay("index_view")
    return render(request, "index.html")
