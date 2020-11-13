from django.contrib import admin
from .models import ForumAnalytics

class ForumAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('log_key',  'log_type', 'date_logged',)
    search_fields = ('log_key',  'log_type', 'resolved',)
    readonly_fields = ('log_key', 'log_value', 'log_type', 'date_logged',)
    ordering = ('-date_logged',)
    list_filter = ('resolved', 'log_key',)
    filter_horizontal = ()
    fieldsets = ()
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('log_value',),
    }),
    )

admin.site.register(ForumAnalytics, ForumAnalyticsAdmin)