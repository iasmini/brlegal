from django.contrib import admin

from .models import CourtDistrict


@admin.register(CourtDistrict)
class CourtDistrictAdmin(admin.ModelAdmin):
    ordering = ('state', 'name')
    list_filter = ['state__name']
    list_display = ['name', 'state']
    search_fields = ['name', 'state__name']
