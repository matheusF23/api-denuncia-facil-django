from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from apps.accounts.api.viewsets import UserViewSet

admin.site.site_header = 'Administração Denúncia Fácil'
admin.site.site_title = 'Denúnncia Fácil'
admin.site.index_title = 'Página Inicial'

router = routers.DefaultRouter()
router.register(r'accounts', UserViewSet, basename='accounts')


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
