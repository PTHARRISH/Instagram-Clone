from django.urls import path

from rbac.views import AssignUserPermissionView
from users.views import (
    BlockUserView,
    CloseFriendView,
    DeleteAccountView,
    FollowActionView,
    FollowersView,
    FollowingView,
    FollowRequestRespondView,
    LoginView,
    LogoutView,
    MuteUserView,
    ProfileView,
    RegisterView,
    UserSettingsView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "admin/assign-permission/",
        AssignUserPermissionView.as_view(),
        name="assign-permission",
    ),
    path("profiles/<str:username>/", ProfileView.as_view(), name="profile-detail"),
    path(
        "profiles/<str:username>/followers/", FollowersView.as_view(), name="followers"
    ),
    path(
        "profiles/<str:username>/following/", FollowingView.as_view(), name="following"
    ),
    path(
        "profiles/<str:username>/follow/",
        FollowActionView.as_view(),
        name="follow-action",
    ),
    path(
        "follow-requests/<int:request_id>/",
        FollowRequestRespondView.as_view(),
        name="follow-request-response",
    ),
    path("block/<int:user_id>/", BlockUserView.as_view()),
    path("mute/<int:user_id>/", MuteUserView.as_view()),
    path("close-friends/<int:user_id>/", CloseFriendView.as_view()),
    path("settings/", UserSettingsView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
]
