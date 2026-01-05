from django.urls import path

from david.api.v1.core.views import HealthCheckView, LogsView


app_name = "core"


urlpatterns = [
    path("healthcheck/", HealthCheckView.as_view(), name="healthcheck"),
    path("logs/", LogsView.as_view(), name="logs"),
]
