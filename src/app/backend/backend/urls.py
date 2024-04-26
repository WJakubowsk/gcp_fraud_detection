from django.contrib import admin
from django.urls import path, include
from authentication.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/user/register/", CreateUserView.as_view(), name="register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("auth-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('transactions/', include('transactions.urls')),
]
