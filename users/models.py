from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel

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


# ---------- Profile Model ----------


class Profile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(max_length=250, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    gender = models.CharField(
        max_length=12,
        choices=GENDER_CHOICES,
        blank=True,
        default="unspecified",
    )
    website = models.URLField(blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"


# ---------- Following & Followers ----------


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
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class FollowRequest(TimeStampedModel):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_follow_requests",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_follow_requests",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"], name="unique_follow_request"
            )
        ]

    def __str__(self):
        return f"{self.from_user.username} requested to follow {self.to_user.username}"


# ---------- Blocking & Muting ----------


class BlockedUser(TimeStampedModel):
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blocked_users"
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blocked_by"
    )

    class Meta:
        unique_together = ["blocker", "blocked"]

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"


class MutedUser(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="muted_users"
    )
    muted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="muted_by"
    )
    mute_posts = models.BooleanField(default=True)
    mute_stories = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} muted {self.muted_user.username}"


# ---------- Close Friends ----------


class CloseFriend(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="close_friends"
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="close_friend_of",
    )

    class Meta:
        unique_together = ["user", "friend"]

    def __str__(self):
        return f"{self.user.username} added {self.friend.username} as a close friend"


# ---------- User Settings ----------


class UserSettings(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings"
    )
    allow_messages_from_followers = models.BooleanField(default=True)
    show_activity_status = models.BooleanField(default=True)
    allow_mentions = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user.username}"
