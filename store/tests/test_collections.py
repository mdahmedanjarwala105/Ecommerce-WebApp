# Every test should have 3 parts AAA - Arrange, Act, Assert
from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):

        client = APIClient()
        response = client.post("/store/collection/", {"title": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self):

        client = APIClient()
        client.force_authenticate(user={})
        response = client.post("/store/collection/", {"title": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
