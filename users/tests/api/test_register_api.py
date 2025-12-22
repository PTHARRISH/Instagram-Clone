import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


# ======================== Register API Tests ========================


@pytest.mark.django_db
class TestRegisterAPI:
    def test_register_success(self, api_client, valid_register_payload):
        url = reverse("register")  # make sure name exists in urls.py
        response = api_client.post(url, valid_register_payload, format="json")

        assert response.status_code == 201
        assert User.objects.filter(username="testuser").exists()
        assert "registered successfully" in response.data["message"]

    def test_register_duplicate_email(
        self, api_client, valid_register_payload, create_user
    ):
        create_user(email="testuser@example.com")
        url = reverse("register")

        response = api_client.post(url, valid_register_payload, format="json")

        assert response.status_code == 400
        assert "email" in response.data

    def test_register_duplicate_mobile(
        self, api_client, valid_register_payload, create_user
    ):
        create_user(mobile="9876543210")
        url = reverse("register")

        response = api_client.post(url, valid_register_payload, format="json")

        assert response.status_code == 400
        assert "mobile" in response.data

    def test_register_password_mismatch(self, api_client, valid_register_payload):
        valid_register_payload["confirm_password"] = "WrongPassword123"
        url = reverse("register")

        response = api_client.post(url, valid_register_payload, format="json")

        assert response.status_code == 400
        assert "confirm_password" in response.data
