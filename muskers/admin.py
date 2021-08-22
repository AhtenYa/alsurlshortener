from django.contrib import admin

from .models import Culink, CulinkStats


class CulinkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['owner']}),
        (None, {'fields': ['longlink_text']}),
        (None, {'fields': ['shortlink_text']}),
        ('Date information', {'fields': ['expiration_date'], 'classes': ['collapse']}),
    ]

    list_display = ('owner', 'longlink_text', 'shortlink_text', 'creation_date', 'expiration_date')
    list_filter = ['creation_date']
    search_fields = ['longlink_text']


class CulinkStatsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['culink']}),
        (None, {'fields': ['redirections']}),
    ]

    list_display = ('culink', 'creation_day', 'redirections')
    list_filter = ['creation_day']
    search_fields = ['culink']


admin.site.register(Culink, CulinkAdmin)
admin.site.register(CulinkStats, CulinkStatsAdmin)
