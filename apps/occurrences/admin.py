from django.contrib import admin

from .models import Occurrence


class OccurrenceAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = ['occurrence_title', 'occurrence_type', 'license_plate',
                    'created_at', 'anonymous', 'status']
    list_display_links = ['occurrence_title']


admin.site.register(Occurrence, OccurrenceAdmin)
