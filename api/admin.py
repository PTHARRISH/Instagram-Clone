from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


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
