import pytest

from django.urls import reverse
from rest_framework import status

from david.tests.factories import DjangoAdminUserFactory


@pytest.mark.django_db
class TestAdmin:
    def setup_method(self):
        self.user = DjangoAdminUserFactory()

    def test_user_changelist(self, client):
        client.force_login(self.user)
        response = client.get(reverse("admin:auth_user_changelist"), follow=True)
        assert response.status_code == status.HTTP_200_OK
