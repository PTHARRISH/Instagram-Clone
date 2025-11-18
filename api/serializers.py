import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import FollowList, Profile, User


class RegisterSerializer(ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "username",
            "email",
            "mobile",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "mobile": {"write_only": True, "required": True},
            "email": {"write_only": True, "required": True},
            "full_name": {"write_only": True, "required": True},
            "username": {"write_only": True, "required": True},
            "confirm_password": {"write_only": True, "required": True},
        }

    def validate_mobile(self, value):
        mobile_str = str(value)
        if len(mobile_str) < 10:
            raise serializers.ValidationError(
                "Mobile number must be at least 10 digits."
            )
        if not mobile_str.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("Mobile number already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        if "@" not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        if len(value) < 5:
            raise serializers.ValidationError("Email is too short.")
        if value.count("@") != 1:
            raise serializers.ValidationError("Enter a valid email address.")
        if regrex := r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$":
            if not re.match(regrex, value):
                raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        if not re.search(r"[a-zA-Z0-9_.+-]", value):
            raise serializers.ValidationError(
                "Password must contain at least one letter, digit, or special character."
            )
        return value

    def validate_confirm_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Confirm Password must be at least 8 characters long."
            )
        if not re.search(r"[a-zA-Z0-9_.+-]", value):
            raise serializers.ValidationError(
                "Confirm Password must contain at least one letter, digit, or special character."
            )
        if password := self.initial_data.get("password"):
            if value != password:
                raise serializers.ValidationError("Passwords do not match.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, min_length=8)

    def validate_identifier(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Username, email, or mobile number is required."
            )
        return value.strip()

    def validate_password(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Password is required.")
        return value


class ProfileSerializer(ModelSerializer):
    # followers_count = serializers.SerializerMethodField()
    # following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "user",
            "bio",
            "avatar",
            "gender",
            "website",
            "is_private",
            "followers",
            "following",
            # "followers_count",
            # "following_count",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate(self, attrs):
        bio = attrs.get("bio", "")
        if bio and len(bio) > 250:
            raise serializers.ValidationError("Bio cannot exceed 250 characters.")
        if website := attrs.get("website", ""):
            url_regex = re.compile(
                r"^(https?:\/\/)?"  # optional http or https scheme
                r"((([a-zA-Z0-9\-_]+\.)+[a-zA-Z]{2,})|"  # domain...
                r"localhost|"  # localhost...
                r"(\d{1,3}\.){3}\d{1,3})"  # ...or ipv4
                r"(:\d+)?(\/[a-zA-Z0-9\-\._~:\/\?#\[\]@!\$&'\(\)\*\+,;%=]*)?$"  # optional port and path
            )
            if not re.match(url_regex, website):
                raise serializers.ValidationError("Enter a valid URL for the website.")
        return attrs

    def get_followers_count(self, obj):
        return FollowList.objects.filter(following=obj.user).count()

    def get_following_count(self, obj):
        return FollowList.objects.filter(follower=obj.user).count()
