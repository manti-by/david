from django.urls import include, path


app_name = "v1"


urlpatterns = [
    path("core/", include("david.api.v1.core.urls"), name="core"),
]
