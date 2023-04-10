from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)

from . import views

router = DefaultRouter()

router.register('account', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', views.ActivationView.as_view(), name='activate')
]