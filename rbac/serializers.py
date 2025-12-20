from django.contrib.auth import get_user_model
from rest_framework import serializers

from rbac.models import PagePermission, Role

User = get_user_model()


class AssignPermissionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()
    url_name = serializers.CharField(max_length=100)
    permission_level = serializers.ChoiceField(
        choices=PagePermission.PERMISSION_CHOICES
    )

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found")
        return value

    def validate_role_id(self, value):
        if not Role.objects.filter(id=value).exists():
            raise serializers.ValidationError("Role not found")
        return value
