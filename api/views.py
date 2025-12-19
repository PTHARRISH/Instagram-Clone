from decimal import Decimal, InvalidOperation

from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import (
    BlockedUser,
    CloseFriend,
    FollowList,
    FollowRequest,
    MutedUser,
    PagePermission,
    Profile,
    Role,
    User,
    UserPermission,
    UserSettings,
)
from api.pagination import DefaultPagination
from api.serializers import (
    AssignPermissionSerializer,
    FollowerSerializer,
    FollowingSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
    UserSettingsSerializer,
)


# ===================== Auth Views =====================
class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"User {user.username} registered successfully."},
                status=201,
            )
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate input using serializer
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        identifier = serializer.validated_data.get("identifier")
        password = serializer.validated_data.get("password")

        user = None
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                try:
                    if identifier.isdigit():
                        mobile_value = Decimal(identifier)
                        user = User.objects.get(mobile=mobile_value)
                except (User.DoesNotExist, ValueError, InvalidOperation):
                    pass

        if not user:
            print(f"[LOGIN] User not found for identifier: {identifier}")
            return Response(
                {"error": "Invalid credentials. User not found."}, status=401
            )

        if not user.check_password(password):
            print(f"[LOGIN] Invalid password for user: {user.username}")
            return Response(
                {"error": "Invalid credentials. Incorrect password."}, status=401
            )

        if not user.is_active:
            return Response({"error": "User account is disabled."}, status=403)

        refresh = RefreshToken.for_user(user)

        print(f"[LOGIN] Success! User: {user.username}")
        return Response(
            {
                "message": "Login successful",
                "username": user.username,
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=200,
        )


# =============== Profile Views ===============


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    parser_classes = [
        JSONParser,
        MultiPartParser,
        FormParser,
    ]

    def get(self, request, username):
        profile = get_object_or_404(
            Profile.objects.select_related("user"), user__username=username
        )
        self.check_object_permissions(request, profile)
        data = self.serializer_class(profile).data
        data["is_owner"] = profile.user == request.user
        # Using View-level annotation to get followers and following counts
        profile = (
            Profile.objects.select_related("user")
            .annotate(
                followers_count=Count("user__follower_set"),
                following_count=Count("user__following_set"),
            )
            .filter(user__username=username)
            .first()
        )
        data["followers_count"] = profile.followers_count
        data["following_count"] = profile.following_count
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        self.check_object_permissions(request, profile)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# ===================== Followers View =====================


class FollowersView(APIView):
    pagination_class = DefaultPagination

    def get(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        search = request.GET.get("search", "")
        queryset = (
            FollowList.objects.filter(following=profile.user)
            .select_related("follower__profile")
            .order_by("-created_at")
        )
        if search:
            queryset = queryset.filter(
                Q(follower__username__icontains=search)
                | Q(follower__full_name__icontains=search)
            )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = FollowerSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def delete(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        self.check_object_permissions(request, profile)
        follower_id = request.data.get("user_id")
        if not follower_id:
            return Response({"detail": "user_id is required"}, status=400)
        try:
            follow = FollowList.objects.get(
                follower_id=follower_id, following=profile.user
            )
            follow.delete()
            return Response({"detail": "Follower removed"}, status=204)
        except FollowList.DoesNotExist:
            return Response({"detail": "User is not a follower"}, status=404)


class FollowingView(APIView):
    pagination_class = DefaultPagination

    def get(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)

        search = request.GET.get("search", "")
        queryset = (
            FollowList.objects.filter(follower=profile.user)
            .select_related("following__profile")
            .order_by("-created_at")
        )
        if search:
            queryset = queryset.filter(
                Q(following__username__icontains=search)
                | Q(following__full_name__icontains=search)
            )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = FollowingSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def delete(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        self.check_object_permissions(request, profile)
        following_id = request.data.get("user_id")
        if not following_id:
            return Response({"detail": "user_id is required"}, status=400)

        try:
            follow = FollowList.objects.get(
                follower=profile.user, following_id=following_id
            )
            follow.delete()
            return Response({"detail": "Unfollowed successfully"}, status=204)

        except FollowList.DoesNotExist:
            return Response({"detail": "You are not following this user"}, status=404)


class FollowActionView(APIView):
    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        if request.user == target_user:
            return Response({"detail": "You cannot follow yourself."}, status=400)
        if FollowList.objects.filter(
            follower=request.user, following=target_user
        ).exists():
            return Response({"detail": "Already following."}, status=400)
        if not target_user.profile.is_private:
            FollowList.objects.create(follower=request.user, following=target_user)
            return Response({"detail": "Followed successfully."}, status=201)
        follow_request, created = FollowRequest.objects.get_or_create(
            from_user=request.user, to_user=target_user
        )
        if not created:
            return Response({"detail": "Follow request already sent."}, status=400)

        return Response({"detail": "Follow request sent."}, status=201)

    def delete(self, request, username):
        target_user = get_object_or_404(User, username=username)
        try:
            req = FollowRequest.objects.get(from_user=request.user, to_user=target_user)
            req.delete()
            return Response({"detail": "Follow request cancelled."}, status=204)
        except FollowRequest.DoesNotExist:
            return Response({"detail": "No follow request found."}, status=404)


class FollowRequestRespondView(APIView):
    def post(self, request, request_id):
        follow_request = get_object_or_404(FollowRequest, id=request_id)

        if follow_request.to_user != request.user:
            return Response({"detail": "Not allowed."}, status=403)
        FollowList.objects.create(
            follower=follow_request.from_user, following=follow_request.to_user
        )

        follow_request.delete()
        return Response({"detail": "Follow request accepted."}, status=201)

    def delete(self, request, request_id):
        follow_request = get_object_or_404(FollowRequest, id=request_id)
        if follow_request.to_user != request.user:
            return Response({"detail": "Not allowed."}, status=403)
        follow_request.delete()
        return Response({"detail": "Follow request rejected."}, status=204)


class AssignUserPermissionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AssignPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=serializer.validated_data["user_id"])
        role = Role.objects.get(id=serializer.validated_data["role_id"])
        url_name = serializer.validated_data["url_name"]
        permission_level = serializer.validated_data["permission_level"]

        # Create/find PagePermission
        page_perm, created = PagePermission.objects.get_or_create(
            url_name=url_name, permission_level=permission_level
        )

        # Create/find UserPermission and link
        user_perm, created = UserPermission.objects.get_or_create(user=user, role=role)
        user_perm.page_permissions.add(page_perm)

        return Response(
            {
                "message": f"Permission {permission_level} for {url_name} assigned to {user.username}",
                "created": created,
            },
            status=status.HTTP_201_CREATED,
        )


# ======================= Block User View =======================
class BlockUserView(APIView):
    def post(self, request, user_id):
        BlockedUser.objects.get_or_create(blocker=request.user, blocked_id=user_id)
        return Response({"detail": "User blocked"}, status=201)

    def delete(self, request, user_id):
        BlockedUser.objects.filter(blocker=request.user, blocked_id=user_id).delete()
        return Response({"detail": "User unblocked"}, status=204)


# ======================= Mute User View =======================
class MuteUserView(APIView):
    def post(self, request, user_id):
        MutedUser.objects.get_or_create(user=request.user, muted_user_id=user_id)
        return Response({"detail": "User muted"}, status=201)

    def delete(self, request, user_id):
        MutedUser.objects.filter(user=request.user, muted_user_id=user_id).delete()
        return Response({"detail": "User unmuted"}, status=204)


# ======================= Close Friends View =======================
class CloseFriendView(APIView):
    def post(self, request, user_id):
        CloseFriend.objects.get_or_create(user=request.user, friend_id=user_id)
        return Response({"detail": "Added to close friends"}, status=201)

    def delete(self, request, user_id):
        CloseFriend.objects.filter(user=request.user, friend_id=user_id).delete()
        return Response({"detail": "Removed from close friends"}, status=204)


# ======================= User Settings View ========================


class UserSettingsView(APIView):
    def get(self, request):
        settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings_obj)
        return Response(serializer.data)

    def patch(self, request):
        settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(
            settings_obj, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ======================== Logout View ========================
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create RefreshToken object and blacklist it
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "message": "Logout successful. Token has been blacklisted.",
                    "redirect_url": "/api/login/",
                },
                status=status.HTTP_200_OK,
            )
        except TokenError as e:
            return Response(
                {"error": f"Invalid token: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ===================== Delete Account View =====================


signer = TimestampSigner()


class DeleteAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return JsonResponse({"error": "Token required"}, status=400)

        try:
            # Verify and check expiration (max_age in seconds = 24h)
            unsigned = signer.unsign(token, max_age=86400)
            user = get_user_model().objects.get(pk=unsigned)
        except SignatureExpired:
            return JsonResponse({"error": "Link expired"}, status=400)
        except (BadSignature, get_user_model().DoesNotExist):
            return JsonResponse({"error": "Invalid link"}, status=400)

        # Delete user and profile
        user.delete()
        return JsonResponse({"message": "Account deleted successfully."}, status=200)
