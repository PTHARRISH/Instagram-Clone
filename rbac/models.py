from django.conf import settings
from django.db import models

# ---------- RBAC Models ----------


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PagePermission(models.Model):
    PERMISSION_CHOICES = [
        ("view", "View Only"),
        ("edit", "Edit"),
        ("delete", "Delete"),
        ("full", "Full Access"),
    ]

    url_name = models.CharField(max_length=100)
    permission_level = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    class Meta:
        unique_together = ["url_name", "permission_level"]

    def __str__(self):
        return f"{self.url_name} - {self.permission_level}"


class UserPermission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rbac_permissions",
    )
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="user_permissions"
    )
    page_permissions = models.ManyToManyField(
        PagePermission, related_name="user_permissions"
    )

    class Meta:
        unique_together = ["user", "role"]

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
