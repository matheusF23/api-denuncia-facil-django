from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['name', 'email']
    list_display_links = ('name', 'email')
    search_fields = ['name', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Informações Pessoais'),
            {'fields': ('name', 'cellphone')}),
        (
            _('Permissões'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Outros Dados'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': {'email', 'password1', 'password2'}
        }),
    )


admin.site.register(User, UserAdmin)
