from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticate(api_client: api_client) -> callable:
    def do_authenticate(is_staff=False) -> callable:
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return do_authenticate
