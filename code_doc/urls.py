from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("snippets.urls")),
    path('', include("polls.urls")),
    path('api/auth/login/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]
