from django.urls import path
from .views import (
    CustomLogoutView,
    CustomRegisterView,
    ChangePasswordView,
    UserListView,
)

urlpatterns = [
    path("logout/", CustomLogoutView.as_view(), name="rest_logout"),
    path("register/", CustomRegisterView.as_view(), name="rest_register"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="rest_change_password",
    ),
    path("users/", UserListView.as_view(), name="user-list"),
]
