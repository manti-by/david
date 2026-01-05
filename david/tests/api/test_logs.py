import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from david.apps.core.models import Log
from david.tests.factories import LogDataFactory, UserFactory


@pytest.mark.django_db
class TestLogsView:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.url = reverse("api:v1:core:logs")

    @pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
    def test_logs__not_allowed_methods(self, method):
        self.client.force_authenticate(self.user)

        test_client_callable = getattr(self.client, method)
        response = test_client_callable(self.url, format="json")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_logs__create(self):
        self.client.force_authenticate(self.user)

        data = LogDataFactory()
        response = self.client.post(self.url, data=data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert Log.objects.exists()
