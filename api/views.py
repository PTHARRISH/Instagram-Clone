from decimal import Decimal, InvalidOperation

from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Profile, User
from api.permissions import IsOwnerOrReadOnly
from api.serializers import LoginSerializer, ProfileSerializer, RegisterSerializer


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

        # Debug logging - this will show in Django terminal
        print("=" * 50)
        print("[LOGIN REQUEST] Received POST request!")
        print(f"[LOGIN REQUEST] IP: {request.META.get('REMOTE_ADDR', 'Unknown')}")
        print(f"[LOGIN REQUEST] Path: {request.path}")
        print(f"[LOGIN REQUEST] Method: {request.method}")
        print(f"[LOGIN REQUEST] Content-Type: {request.content_type}")
        print(f"[LOGIN REQUEST] Data: {dict(request.data)}")
        print("=" * 50)

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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
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
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)
        self.check_object_permissions(request, profile)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# ======================== Logout View ========================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

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
