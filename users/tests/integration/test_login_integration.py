from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_login_creates_valid_jwt_tokens():
    User.objects.create_user(
        username="jwtuser",
        email="jwt@example.com",
        mobile=Decimal("9999999999"),
        password="StrongPass123",
    )

    client = APIClient()
    response = client.post(
        reverse("login"),
        {"identifier": "jwtuser", "password": "StrongPass123"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["tokens"]["access"]
    assert response.data["tokens"]["refresh"]
