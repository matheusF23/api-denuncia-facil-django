from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
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
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
