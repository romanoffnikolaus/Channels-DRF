from django.urls import path
from .views import ForumPostView

urlpatterns = [
    path('forum/', ForumPostView.as_view())
]