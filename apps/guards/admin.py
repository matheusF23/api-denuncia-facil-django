from django.contrib import admin

from .models import Guard


class GuardAdmin(admin.ModelAdmin):
    ordering = ['cod_guard']
    list_display = ['name', 'cod_guard']
    list_display_links = ['name']


admin.site.register(Guard, GuardAdmin)
