from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title='EnactusAnimalProject',
        description='Платформа по услугам для животных',
        default_version='v1',
       
    ), public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger')),
    path('', include('account.urls')),
    path('', include('announcement.urls')),
    path('', include('categories.urls')),
    path('', include('news.urls')),
    path('', include('catalog.urls')),
    path('', include('review.urls')),
    path('chat/', include('chat.urls')),
    path('__debug__/', include('debug_toolbar.urls'))
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)