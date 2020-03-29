from django.contrib import admin

from .models import State, City
# Register your models here.

class StateAdmin(admin.ModelAdmin):
    fields = ( 'name',)
    readonly_fields = ('created', 'updated')
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    date_hierarchy = 'updated' # Jerarquizar por fechas
    list_filter = ('name',)

admin.site.register(State, StateAdmin)


class CityAdmin(admin.ModelAdmin):
    autocomplete_fields = ('state',)
    fields = ( 'name', 'zip_city', 'ddn', 'state')
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'zip_city', 'ddn', 'state')
    ordering = ('name',)
    search_fields = ('name',)
    date_hierarchy = 'updated' # Jerarquizar por fechas
    list_filter = ('name',)
    list_editable = ('zip_city', 'ddn')
    list_select_related = ('state',)

admin.site.register(City, CityAdmin)
