from django.urls import path
from .views import CustomLogoutView, CustomRegisterView

urlpatterns = [
    path("logout/", CustomLogoutView.as_view(), name="rest_logout"),
    path("register/", CustomRegisterView.as_view(), name="rest_register"),
]
