from dj_rest_auth.views import LogoutView
from dj_rest_auth.registration.views import RegisterView
from .serializers import (
    CustomRegisterSerializer,
    ChangePasswordSerializer,
    CustomUserSerializer,
)
from rest_framework import filters
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

# Create your views here.


class CustomLogoutView(LogoutView):
    def logout(self, request):
        response = super().logout(request)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()

        refresh_token = response.cookies.get("refresh")

        if refresh_token:
            response.data["refresh"] = refresh_token.value

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Get refresh token from body first, fall back to cookie
        refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Pass it directly to the serializer
        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        # Also set the new refresh token as a cookie
        new_refresh = serializer.validated_data.get("refresh")
        if new_refresh:
            response.set_cookie(
                "refresh",
                new_refresh,
                httponly=True,
                secure=True,
                samesite="None",
                max_age=7 * 24 * 60 * 60,
            )

        return response


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = CustomUser

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()

            return Response(
                {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Password updated successfully",
                    "data": [],
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email", "first_name", "last_name"]
