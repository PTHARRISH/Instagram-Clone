import pytest

from users.serializers import RegisterSerializer

# ======================== Register Serializer Tests ========================


@pytest.mark.django_db
class TestRegisterSerializer:
    def test_valid_serializer(self, valid_register_payload):
        serializer = RegisterSerializer(data=valid_register_payload)
        assert serializer.is_valid() is True

    def test_invalid_email(self, valid_register_payload):
        valid_register_payload["email"] = "invalid-email"
        serializer = RegisterSerializer(data=valid_register_payload)

        assert serializer.is_valid() is False
        assert "email" in serializer.errors

    def test_short_password(self, valid_register_payload):
        valid_register_payload["password"] = "123"
        valid_register_payload["confirm_password"] = "123"
        serializer = RegisterSerializer(data=valid_register_payload)

        assert serializer.is_valid() is False
        assert "password" in serializer.errors

    def test_password_mismatch(self, valid_register_payload):
        valid_register_payload["confirm_password"] = "Mismatch123"
        serializer = RegisterSerializer(data=valid_register_payload)

        assert serializer.is_valid() is False
        assert "confirm_password" in serializer.errors
