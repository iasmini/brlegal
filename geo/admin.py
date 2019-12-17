from django.contrib import admin

from .models import CourtDistrict, State


@admin.register(CourtDistrict)
class CourtDistrictAdmin(admin.ModelAdmin):
    ordering = ('state', 'name')
    list_filter = ['state__name']
    list_display = ['name', 'state']
    search_fields = ['name', 'state__name']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
