from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)

from . import views

router = DefaultRouter()

router.register('account', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('account/login/', TokenObtainPairView.as_view()),
    path('account/refresh', TokenRefreshView.as_view())
]