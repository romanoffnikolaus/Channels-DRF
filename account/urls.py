from django.urls import path, include
from rest_framework.routers import DefaultRouter

import views

router = DefaultRouter()

router.register('user', views.UserViewSet)


urlpatterns = [
    path('account/', include(router.urls))
]