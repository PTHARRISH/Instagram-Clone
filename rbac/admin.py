from django.contrib import admin

from rbac.models import PagePermission, Role, UserPermission


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin for Role model used in RBAC."""

    list_display = ["id", "name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(PagePermission)
class PagePermissionAdmin(admin.ModelAdmin):
    """Admin for PagePermission (URL + permission level)."""

    list_display = ["id", "url_name", "permission_level"]
    list_filter = ["permission_level"]
    search_fields = ["url_name"]
    ordering = ["url_name"]


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """Admin for UserPermission (user + role + many page permissions)."""

    list_display = ["id", "user", "role"]
    list_filter = ["role"]
    search_fields = ["user__username", "user__email", "role__name"]
    filter_horizontal = ["page_permissions"]  # Better UI for ManyToMany

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user", "role").prefetch_related("page_permissions")
