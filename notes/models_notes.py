# from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from django.db import models
# from django.utils import timezone

# # ---------- Base mixins ----------


# class TimeStampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


# # ---------- User & Profile ----------


# class User(AbstractUser):
#     """
#     Extends AbstractUser; adds full_name and mobile.
#     """

#     full_name = models.CharField(
#         max_length=30, null=False, blank=False, verbose_name="Full Name"
#     )
#     mobile = models.DecimalField(
#         max_digits=10,
#         decimal_places=0,
#         unique=True,
#         blank=False,
#         null=False,
#         verbose_name="Mobile Number",
#     )

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email", "mobile", "full_name"]

#     def __str__(self):
#         return str(self.username)


# GENDER_CHOICES = [
#     ("M", "Male"),
#     ("F", "Female"),
# ]


# class Profile(TimeStampedModel):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
#     )
#     bio = models.TextField(max_length=250, blank=True, null=True)
#     avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
#     gender = models.CharField(
#         max_length=12, choices=GENDER_CHOICES, null=True, blank=True
#     )
#     website = models.URLField(blank=True, null=True)
#     is_private = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Profile of {self.user.username}"


# # ---------- Social graph ----------


# class Follow(TimeStampedModel):
#     follower = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
#     )
#     following = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["follower", "following"], name="unique_follow_pair"
#             )
#         ]
#         indexes = [
#             models.Index(fields=["follower", "following"]),
#         ]

#     def __str__(self):
#         return f"{self.follower} -> {self.following}"


# # ---------- Posts & media ----------

# MEDIA_TYPE_CHOICES = [
#     ("IMAGE", "Image"),
#     ("VIDEO", "Video"),
# ]


# class Post(TimeStampedModel):
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
#     )
#     caption = models.TextField(max_length=2200, blank=True)
#     location = models.CharField(max_length=120, blank=True)
#     is_archived = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Post {self.id} by {self.author}"


# class PostMedia(TimeStampedModel):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
#     file = models.FileField(upload_to="posts/%Y/%m/")
#     media_type = models.CharField(max_length=8, choices=MEDIA_TYPE_CHOICES)
#     order = models.PositiveIntegerField(default=0)
#     width = models.PositiveIntegerField(null=True, blank=True)
#     height = models.PositiveIntegerField(null=True, blank=True)
#     duration_ms = models.PositiveIntegerField(null=True, blank=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["post", "order"], name="unique_media_order_per_post"
#             )
#         ]
#         ordering = ["order"]

#     def __str__(self):
#         return f"Media {self.id} of Post {self.post_id}"


# # ---------- Comments & likes ----------


# class Comment(TimeStampedModel):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
#     author = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
#     )
#     text = models.TextField(max_length=1000)
#     parent = models.ForeignKey(
#         "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True
#     )
#     is_deleted = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Comment {self.id} on Post {self.post_id}"


# class PostLike(TimeStampedModel):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_likes"
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=["post", "user"], name="unique_post_like")
#         ]

#     def __str__(self):
#         return f"{self.user} likes Post {self.post_id}"


# class CommentLike(TimeStampedModel):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_likes"
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["comment", "user"], name="unique_comment_like"
#             )
#         ]

#     def __str__(self):
#         return f"{self.user} likes Comment {self.comment_id}"


# # ---------- Hashtags & tagging ----------


# class Hashtag(TimeStampedModel):
#     name = models.CharField(max_length=100, unique=True, db_index=True)

#     def __str__(self):
#         return f"#{self.name}"


# class PostHashtag(TimeStampedModel):
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name="post_hashtags"
#     )
#     hashtag = models.ForeignKey(
#         Hashtag, on_delete=models.CASCADE, related_name="tagged_posts"
#     )

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["post", "hashtag"], name="unique_post_hashtag"
#             )
#         ]


# class PostUserTag(TimeStampedModel):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="user_tags")
#     tagged_user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="tagged_in_posts",
#     )
#     pos_x = models.FloatField(null=True, blank=True)  # optional placement in media
#     pos_y = models.FloatField(null=True, blank=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["post", "tagged_user"], name="unique_user_tag_per_post"
#             )
#         ]


# # ---------- Saves / collections ----------


# class SavedPost(TimeStampedModel):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_posts"
#     )
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="saves")
#     collection = models.CharField(max_length=80, blank=True, default="")

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["user", "post", "collection"],
#                 name="unique_saved_post_in_collection",
#             )
#         ]


# # ---------- Stories ----------


# def _story_expires():
#     return timezone.now() + timezone.timedelta(hours=24)


# class Story(TimeStampedModel):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stories"
#     )
#     file = models.FileField(upload_to="stories/%Y/%m/")
#     media_type = models.CharField(max_length=8, choices=MEDIA_TYPE_CHOICES)
#     expires_at = models.DateTimeField(default=_story_expires, db_index=True)
#     is_archived = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Story {self.id} by {self.user}"


# class StoryView(TimeStampedModel):
#     story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="views")
#     viewer = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="story_views"
#     )
#     viewed_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["story", "viewer"], name="unique_story_view"
#             )
#         ]


# # ---------- Reels ----------


# class Reel(TimeStampedModel):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reels"
#     )
#     video = models.FileField(upload_to="reels/%Y/%m/")
#     caption = models.TextField(max_length=2200, blank=True)
#     cover = models.ImageField(upload_to="reels/covers/%Y/%m/", blank=True, null=True)
#     duration_ms = models.PositiveIntegerField(null=True, blank=True)

#     def __str__(self):
#         return f"Reel {self.id} by {self.user}"


# # ---------- Notifications (generic target) ----------


# class Notification(TimeStampedModel):
#     recipient = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
#     )
#     actor = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="actor_notifications",
#     )
#     verb = models.CharField(max_length=64)  # e.g., 'liked', 'commented', 'followed'
#     # Generic target (Post, Comment, etc.)
#     content_type = models.ForeignKey(
#         ContentType, on_delete=models.CASCADE, null=True, blank=True
#     )
#     object_id = models.PositiveBigIntegerField(null=True, blank=True)
#     target = GenericForeignKey("content_type", "object_id")
#     is_read = models.BooleanField(default=False)

#     class Meta:
#         indexes = [
#             models.Index(fields=["recipient", "is_read", "-created_at"]),
#         ]

#     def __str__(self):
#         return f"Notify {self.recipient} about {self.verb}"


# # ---------- Direct messages ----------


# class Thread(TimeStampedModel):
#     title = models.CharField(max_length=120, blank=True)
#     participants = models.ManyToManyField(
#         settings.AUTH_USER_MODEL, related_name="threads", blank=True
#     )

#     def __str__(self):
#         return f"Thread {self.id}"


# class Message(TimeStampedModel):
#     thread = models.ForeignKey(
#         Thread, on_delete=models.CASCADE, related_name="messages"
#     )
#     sender = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages_sent"
#     )
#     text = models.TextField(blank=True)
#     attachment = models.FileField(upload_to="messages/%Y/%m/", blank=True, null=True)
#     is_read = models.BooleanField(default=False)

#     class Meta:
#         indexes = [
#             models.Index(fields=["thread", "created_at"]),
#         ]

#     def __str__(self):
#         return f"Msg {self.id} in Thread {self.thread_id}"


# # ---------- Profile auto-create signal (keep in signals.py in production) ----------

# from django.db.models.signals import post_save
# from django.dispatch import receiver


# @receiver(post_save, sender=User, dispatch_uid="create_profile_once")
# def create_profile_on_user_create(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user=instance)
