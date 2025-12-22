import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_register_creates_user_in_database(api_client, valid_register_payload):
    response = api_client.post(
        reverse("register"),
        valid_register_payload,
        format="json",
    )

    assert response.status_code == 201

    user = User.objects.get(username="testuser")

    # DB assertions
    assert user.email == "testuser@example.com"
    assert user.mobile == int(valid_register_payload["mobile"])
    assert user.full_name == "Test User"

    # Password must be hashed
    assert user.password != valid_register_payload["password"]
    assert user.check_password(valid_register_payload["password"]) is True


def test_register_does_not_store_confirm_password(api_client, valid_register_payload):
    api_client.post(
        reverse("register"),
        valid_register_payload,
        format="json",
    )

    user = User.objects.get(username="testuser")

    assert not hasattr(user, "confirm_password")
