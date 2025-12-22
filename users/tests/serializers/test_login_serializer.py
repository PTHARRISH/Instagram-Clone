import pytest

from users.serializers import LoginSerializer

pytestmark = pytest.mark.django_db


def test_login_serializer_valid_data():
    serializer = LoginSerializer(
        data={"identifier": "testuser", "password": "TestPass123"}
    )
    assert serializer.is_valid()


def test_login_serializer_missing_identifier():
    serializer = LoginSerializer(data={"password": "TestPass123"})
    assert not serializer.is_valid()
    assert "identifier" in serializer.errors


def test_login_serializer_missing_password():
    serializer = LoginSerializer(data={"identifier": "testuser"})
    assert not serializer.is_valid()
    assert "password" in serializer.errors


def test_login_serializer_password_too_short():
    serializer = LoginSerializer(data={"identifier": "testuser", "password": "123"})
    assert not serializer.is_valid()
    assert "password" in serializer.errors
