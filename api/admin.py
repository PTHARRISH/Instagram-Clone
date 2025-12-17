from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Role, PagePermission, UserPermission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    
    # Fields to display in list view
    list_display = ['username', 'email', 'full_name', 'mobile', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'full_name', 'mobile']
    ordering = ['-date_joined']
    
    # Fieldsets for add/edit form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('full_name', 'mobile')
        }),
    )
    
    # Fieldsets for creating new user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('full_name', 'mobile', 'email')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for Profile model"""
    
    list_display = ['user', 'gender', 'bio', 'avatar']
    list_filter = ['gender']
    search_fields = ['user__username', 'user__email', 'bio']
    raw_id_fields = ['user']  # Use widget for user selection
    readonly_fields = ['user']  # Make user read-only after creation
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'avatar', 'gender')
        }),
    )



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin for Role model used in RBAC"""

    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(PagePermission)
class PagePermissionAdmin(admin.ModelAdmin):
    """Admin for PagePermission (URL + permission level)"""

    list_display = ['id', 'url_name', 'permission_level']
    list_filter = ['permission_level']
    search_fields = ['url_name']
    ordering = ['url_name']


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """Admin for UserPermission (user + role + many page permissions)"""

    list_display = ['id', 'user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email', 'role__name']
    filter_horizontal = ['page_permissions']  # Better UI for ManyToMany

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'role').prefetch_related('page_permissions')