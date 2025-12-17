from django.urls import resolve
from rest_framework.permissions import BasePermission

from .models import UserPermission


class DynamicPagePermission(BasePermission):
    HTTP_TO_PERMISSION = {
        "GET": "view",
        "POST": "edit",
        "PUT": "edit",
        "PATCH": "edit",
        "DELETE": "delete",
    }

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Get required permission for this HTTP method
        required_perm = self.HTTP_TO_PERMISSION.get(request.method, "view")

        # Get current page/URL
        current_url = resolve(request.path_info).url_name or request.path.strip(
            "/"
        ).replace("/", "_")
        # Fetch user permissions from DB
        user_perms = UserPermission.objects.filter(user=request.user).prefetch_related(
            "page_permissions"
        )

        for uperm in user_perms:
            if uperm.page_permissions.filter(
                url_name__iexact=current_url,
                permission_level__in=[required_perm, "full"],
            ).exists():
                return True

        return False
