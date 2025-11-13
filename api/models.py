from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# ---------- Base mixins ----------


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ---------- User and Profile Models ----------


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    AbstractUser already includes: username, email, password, is_staff, is_superuser, etc.
    We just add our custom fields here.
    """

    full_name = models.CharField(
        max_length=150, null=False, blank=False, verbose_name="Full Name"
    )
    mobile = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Mobile Number",
    )

    # AbstractUser already has: username, email, password, is_staff, is_superuser, is_active
    # So we don't need to redefine them

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "mobile", "full_name"]  # password is handled separately

    def __str__(self):
        return str(self.username)


GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
]


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    gender = models.CharField(
        max_length=12, choices=GENDER_CHOICES, null=True, blank=True
    )
    website = models.URLField(blank=True, null=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"


class FollowList(TimeStampedModel):
    """A model to represent follower-following relationships between users."""

    """Follower follows Following it is a one way relationship"""
    """Why? Because if A follows B it does not mean B follows A."""
    """So we need to create two entries in the FollowList model to represent both relationships."""

    # For example: A follows B
    #     FollowList entry 1: follower=A, following=B
    #     FollowList entry 2: follower=B, following=A (if B follows A)

    """Why not a ManyToManyField?"""
    """Using ManyToManyField would make it difficult to enforce unique constraints
    and to query the relationships efficiently."""
    """Also, with this model we can easily extend it in the future to add more fields
    like 'since when' the follow happened, notifications, etc.      
    """

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following_set"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower_set"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow_pair"
            )
        ]
        indexes = [
            models.Index(fields=["follower", "following"]),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
