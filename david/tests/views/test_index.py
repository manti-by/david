import pytest

from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestIndex:
    def test_dashboard(self, client):
        response = client.get(reverse("index"), follow=True)
        assert response.status_code == status.HTTP_200_OK
