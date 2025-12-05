from django.urls import path

from api.views import (
    DeleteAccountView,
    FollowActionView,
    FollowersView,
    FollowingView,
    FollowRequestRespondView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
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
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
]
