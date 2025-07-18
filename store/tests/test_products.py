"""Test cases for creating and retrieving products."""

# Every test should have 3 parts AAA - Arrange, Act, Assert
from typing import Callable
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from model_bakery import baker
from store.models import Product, Collection
import pytest


@pytest.fixture
def create_product(api_client: APIClient) -> Callable:
    """
    Fixture to return a function that sends a POST request to create a product.

    Args:
        api_client (APIClient): The DRF test client.

    Returns:
        Callable: Function that accepts product data as a dictionary and returns the API response.
    """

    def do_create_product(product: dict) -> Response:
        """
        Sends a POST request to create a product.

        Args:
            product (dict): The payload for the product.

        Returns:
            Response: The response from the API.
        """

        return api_client.post("/store/product/", product)

    return do_create_product


@pytest.mark.django_db
class TestCreatePoduct:
    """Test cases for creating a product."""

    def test_if_user_is_anonymous_returns_401(self, create_product: Callable) -> None:
        """Should return 401 if the user is not authenticated."""

        collection = baker.make(Collection)

        payload = {
            "title": "Test Product",
            "slug": "test-product",
            "price": "19.99",
            "collection": collection.id,
        }

        response = create_product(payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, create_product: Callable, authenticate: Callable
    ) -> None:
        """Should return 403 if the user is authenticated but not an admin."""

        collection = baker.make(Collection)

        payload = {
            "title": "Test Product",
            "slug": "test-product",
            "price": "19.99",
            "collection": collection.id,
        }

        authenticate()

        response = create_product(payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_not_admin_returns_400(
        self, create_product: Callable, authenticate: Callable
    ) -> None:
        """Should return 400 if the product data is invalid."""

        authenticate(is_staff=True)

        collection = baker.make(Collection)

        payload = {
            "title": "",
            "slug": "",
            "price": "",
            "collection": "",
        }

        response = create_product(payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(
        self, create_product: Callable, authenticate: Callable
    ) -> None:
        """Should return 201 if the product is created with valid data."""

        authenticate(is_staff=True)

        collection = baker.make(Collection)

        payload = {
            "title": "Test Product",
            "slug": "test-product",
            "price": "19.99",
            "collection": collection.id,
        }

        response = create_product(payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveProduct:
    """Test cases for retrieving a product."""

    def test_if_collection_exists_returns_200(self, api_client: APIClient) -> None:
        """Should return 200 if the requested product exists."""

        product = baker.make(Product)

        response = api_client.get(f"/store/product/{product.pk}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == product.title
        assert response.data["price"] == product.price
        assert response.data["collection"] == product.collection.id

    def test_if_collection_does_not_exits_returns_404(
        self, api_client: APIClient
    ) -> None:
        """Should return 404 if the requested product does not exist."""

        response = api_client.get(
            "/store/product/9999/"
        )  # Here 9999 is the assumption that it is a non existing collection primary key

        assert response.status_code == status.HTTP_404_NOT_FOUND
