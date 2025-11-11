from decimal import Decimal, InvalidOperation

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User
from api.serializers import LoginSerializer, RegisterSerializer


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
