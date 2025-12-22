import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
pytestmark = pytest.mark.django_db


# ---------- SUCCESS CASES ----------


def test_login_with_username_success(api_client, active_user):
    response = api_client.post(
        reverse("login"),
        {"identifier": "testuser", "password": "TestPass123"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["username"] == "testuser"
    assert "access" in response.data["tokens"]
    assert "refresh" in response.data["tokens"]


def test_login_with_email_success(api_client, active_user):
    response = api_client.post(
        reverse("login"),
        {"identifier": "test@example.com", "password": "TestPass123"},
        format="json",
    )

    assert response.status_code == 200


def test_login_with_mobile_success(api_client, active_user):
    response = api_client.post(
        reverse("login"),
        {"identifier": "9876543210", "password": "TestPass123"},
        format="json",
    )

    assert response.status_code == 200


# ---------- FAILURE CASES ----------


def test_login_user_not_found(api_client):
    response = api_client.post(
        reverse("login"),
        {"identifier": "unknown", "password": "TestPass123"},
        format="json",
    )

    assert response.status_code == 401
    assert "Invalid credentials" in response.data["error"]


def test_login_wrong_password(api_client, active_user):
    response = api_client.post(
        reverse("login"),
        {"identifier": "testuser", "password": "WrongPass123"},
        format="json",
    )

    assert response.status_code == 401


def test_login_inactive_user(api_client, inactive_user):
    response = api_client.post(
        reverse("login"),
        {"identifier": "inactiveuser", "password": "TestPass123"},
        format="json",
    )

    assert response.status_code == 403
