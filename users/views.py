from dj_rest_auth.views import LogoutView
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer, ChangePasswordSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
# Create your views here.


class CustomLogoutView(LogoutView):
    def logout(self, request):
        response = super().logout(request)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


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
