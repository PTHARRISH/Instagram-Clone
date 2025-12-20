from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from rbac.models import PagePermission, Role, UserPermission
from rbac.serializers import AssignPermissionSerializer

User = get_user_model()


class AssignUserPermissionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AssignPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=serializer.validated_data["user_id"])
        role = Role.objects.get(id=serializer.validated_data["role_id"])
        url_name = serializer.validated_data["url_name"]
        permission_level = serializer.validated_data["permission_level"]

        # Create/find PagePermission
        page_perm, created = PagePermission.objects.get_or_create(
            url_name=url_name, permission_level=permission_level
        )

        # Create/find UserPermission and link
        user_perm, created = UserPermission.objects.get_or_create(user=user, role=role)
        user_perm.page_permissions.add(page_perm)

        return Response(
            {
                "message": f"Permission {permission_level} for {url_name} assigned to {user.username}",
                "created": created,
            },
            status=status.HTTP_201_CREATED,
        )
