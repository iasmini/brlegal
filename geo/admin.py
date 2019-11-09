from django.contrib import admin

from .models import CourtDistrict


@admin.register(CourtDistrict)
class CourtDistrictAdmin(admin.ModelAdmin):
    ordering = ('state', 'name')
    list_filter = ['state']
    list_display = ['name', 'state']
    search_fields = ['name', 'state']
