"""Test cases for creating and retrieving collections."""

# Every test should have 3 parts AAA - Arrange, Act, Assert
from typing import Callable
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from model_bakery import baker
from store.models import Collection
import pytest


@pytest.fixture
def create_collection(api_client: APIClient) -> Callable:
    """
    Fixture to return a function that sends a POST request to create a collection.

    Args:
        api_client (APIClient): The DRF test client.

    Returns:
        Callable: Function that accepts collection data as a dictionary and returns the API response.
    """

    def do_create_collection(
        collection: dict,
    ) -> Response:
        """
        Sends a POST request to create a collection.

        Args:
            collection (dict): The payload for the collection.

        Returns:
            Response: The response from the API.
        """

        return api_client.post("/store/collection/", collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    """Test cases for creating a collection."""

    def test_if_user_is_anonymous_returns_401(
        self, create_collection: Callable
    ) -> None:
        """Should return 401 if the user is not authenticated."""

        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self,
        create_collection: Callable,
        authenticate: Callable,
    ) -> None:
        """Should return 403 if the user is authenticated but not an admin."""

        authenticate()

        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(
        self,
        create_collection: Callable,
        authenticate: Callable,
    ) -> None:
        """Should return 400 if the collection data is invalid (e.g., missing title)."""

        authenticate(is_staff=True)

        response = create_collection({"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_data_is_valid_returns_201(
        self,
        create_collection: Callable,
        authenticate: Callable,
    ) -> None:
        """Should return 201 if the collection is created with valid data."""

        authenticate(is_staff=True)

        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    """Test cases for retrieving a collection."""

    def test_if_collection_exists_returns_200(self, api_client: APIClient) -> None:
        """Should return 200 if the requested collection exists."""

        collection = baker.make(Collection)

        response = api_client.get(f"/store/collection/{collection.pk}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.pk,
            "title": collection.title,
            "product_count": 0,
        }

    def test_if_collection_does_not_exits_returns_404(
        self, api_client: APIClient
    ) -> None:
        """Should return 404 if the requested collection does not exist."""

        response = api_client.get(
            "/store/collection/9999/"
        )  # Here 9999 is the assumption that it is a non existing collection primary key

        assert response.status_code == status.HTTP_404_NOT_FOUND
