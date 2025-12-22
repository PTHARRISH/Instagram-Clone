from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

# Fixtures

# ======================== API Client Fixture ========================


@pytest.fixture
def api_client():
    return APIClient()


# ======================== Register Payload & User Creation Fixtures ========================


@pytest.fixture
def valid_register_payload():
    return {
        "full_name": "Test User",
        "username": "testuser",
        "email": "testuser@example.com",
        "mobile": "9876543210",
        "password": "Password@123",
        "confirm_password": "Password@123",
    }


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        return User.objects.create_user(
            username=kwargs.get("username", "existinguser"),
            email=kwargs.get("email", "existing@example.com"),
            mobile=kwargs.get("mobile", "9999999999"),
            password=kwargs.get("password", "Password@123"),
            full_name=kwargs.get("full_name", "Existing User"),
        )

    return _create_user


# ======================== User Fixtures ========================


@pytest.fixture
def active_user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        mobile=Decimal("9876543210"),
        password="TestPass123",
        is_active=True,
    )


@pytest.fixture
def inactive_user():
    return User.objects.create_user(
        username="inactiveuser",
        email="inactive@example.com",
        mobile=Decimal("9123456789"),
        password="TestPass123",
        is_active=False,
    )
