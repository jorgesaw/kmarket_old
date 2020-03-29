from django.contrib import admin

from .models import DailyBalance
from .forms import OverheadForm
# Register your models here.

class DailyBalanceAdmin(admin.ModelAdmin):
    fields = ('date_balance', 'init_cash', 'custom_value')
    list_display = ('date_balance', 'init_cash', 'show_overheads')
    ordering = ('-date_balance',)
    search_fields = ('date_balance',)
    date_hierarchy = 'date_balance' # Jerarquizar por fechas
    list_filter = ('date_balance',)
    #form = OverheadForm

    def show_overheads(self, obj):
        return "GASTOS"
    show_overheads.short_description = "gastos"
    
admin.site.register(DailyBalance, DailyBalanceAdmin)