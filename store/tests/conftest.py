from typing import Callable
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticate(api_client: APIClient) -> Callable:
    def do_authenticate(is_staff: bool = False) -> None:
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return do_authenticate
