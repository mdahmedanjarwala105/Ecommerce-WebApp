"""Test cases for creating a collection."""

# Every test should have 3 parts AAA - Arrange, Act, Assert
from typing import Callable
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.http import HttpRequest


@pytest.fixture
def create_collection(api_client: APIClient) -> Callable:
    """This fixture returns a function that can be used to create a collection."""

    def do_create_collection(
        collection: dict,
    ) -> HttpRequest:
        return api_client.post("/store/collection/", collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    """Test cases for creating a collection."""

    def test_if_user_is_anonymous_returns_401(
        self, create_collection: Callable
    ) -> None:
        """Test if an anonymous user tries to create a collection."""

        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self,
        create_collection: Callable,
        authenticate: Callable,
    ) -> None:
        """Test if a user who is not an admin tries to create a collection."""

        authenticate()

        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(
        self,
        create_collection: Callable,
        authenticate: Callable,
    ) -> None:
        """Test if a user who is an admin tries to create a collection with invalid data."""

        authenticate(is_staff=True)

        response = create_collection({"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(
        self,
        create_collection: Callable,
        authenticate: Callable,
    ) -> None:
        """Test if a user who is an admin tries to create a collection with valid data."""

        authenticate(is_staff=True)

        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
