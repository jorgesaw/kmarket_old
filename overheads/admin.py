from django.contrib import admin
from django.utils.html import format_html

from .models import Overhead, ItemOverhead
# Register your models here.
class ItemOverheadAdmin(admin.TabularInline):
    model = ItemOverhead
    fields = ('name', 'value')
    list_display = ('name', 'value')
    ordering = ('id',)
    list_editable = ('name', 'value')
    extra = 1

class OverheadAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( ('date_overhead', 'total'), )
        }),
    )
    readonly_fields = ('created', 'updated', 'total')
    list_display = ('date_overhead', 'color_html_total_display')
    ordering = ('-date_overhead',)
    search_fields = ('date_overhead',)
    date_hierarchy = 'date_overhead' # Jerarquizar por fechas
    list_filter = ('date_overhead',)
    inlines = [ItemOverheadAdmin,]

    def color_html_total_display(self, obj):
        return format_html(
            f'<span style="color: red">{obj.total}</span>'
        )
    color_html_total_display.short_description = 'Total'

    def color_html_remaining_cash_display(self, obj):
        return format_html(
            f'<span style="color: green">{obj.total}</span>'
        )
    color_html_remaining_cash_display.short_description = 'Efectivo restante'
    
admin.site.register(Overhead, OverheadAdmin)
