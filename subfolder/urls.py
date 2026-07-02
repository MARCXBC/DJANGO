from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .views import *

urlpatterns = [
    path("register/", signup),
    path("verify_email/", verify_user),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path ("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/", get_user),
    path("update/", update_user),
    path("delete/<int:id>/", delete_user),
    path("password-reset/", reset_password),
]