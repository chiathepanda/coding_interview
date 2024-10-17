from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter(trailing_slash=False)
router.register(r'cafes', CafeViewSet, basename="cafe")

urlpatterns = [
    path('', include(router.urls)),
    path('cafe', CafeViewSet.as_view(
        {
            'post': 'create_cafe',
            'put': 'update_cafe',
            'delete': 'delete_cafe'
         }), name='cafe-api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)