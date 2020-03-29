from django.contrib import admin

from .models import Sale, SaleWithDailyBalance, SaleSummary, ItemSale
from payments.models import Payment
from .actions import fiscal_bill_emited, fiscal_bill_not_emited
# Register your models here.

class PaymentAdmin(admin.TabularInline):
    model = Payment
    #autocomplete_fields = ('payment_type',)
    fields = ('payment_type',)
    ordering = ('id',)
    #list_editable = ('amount',)
    list_select_related = ('payment_type',)
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Mostrar por defecto el primer método de pago (CASH - EFECTIVO)"""
        if db_field.name == 'payment_type':
            kwargs['initial'] = 1
        return super(PaymentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ItemSaleAdmin(admin.TabularInline):
    model = ItemSale
    autocomplete_fields = ('product',)
    #autocomplete_fields = ('product_price',) Si son varios precios por producto
    fields = ('product', 'quantity', 'discount', 'value')
    #fields = ('product_price', 'quantity', 'discount', 'value')
    readonly_fields = ('value',)
    list_display = ('product', 'show_price', 'quantity', 'discount', 'value')
    #list_display = ('product', 'show_price', 'quantity', 'discount', 'value')
    ordering = ('id',)
    list_editable = ('quantity', 'discount')
    list_select_related = ('product',)
    extra = 1

    def show_price(self, obj):
        return obj.actual_price
    show_price.short_description = 'Precio'

class SaleAdmin(admin.ModelAdmin):
    #raw_id_fields = ('customer',)
    autocomplete_fields = ('customer',)
    fieldsets = (
        ('Datos básicos', {
            'fields': ( ('number_sale', 'date_sale', 'fiscal_bill'), ('customer', 'value') )
        }),
        ('Datos complementarios', {
            'classes': ('collapse',),
            'fields': ('discount', 'tax',),
        }),
    )
    readonly_fields = ('created', 'updated', 'value')
    list_display = ('number_sale', 'date_sale', 'customer', 'fiscal_bill', 'value')
    ordering = ('date_sale',)
    search_fields = ('number_sale', 'customer__id_card', 'customer__last_name')
    date_hierarchy = 'date_sale' # Jerarquizar por fechas
    list_filter = ('date_sale', 'customer__id_card', 'customer__last_name')
    list_select_related = ('customer',)
    actions = [fiscal_bill_emited, fiscal_bill_not_emited]
    inlines = [ItemSaleAdmin, PaymentAdmin]

admin.site.register(Sale, SaleAdmin)

class SaleWithDailyBalanceAdmin(SaleAdmin):
    list_select_related = ('daily_balance',)

admin.site.register(SaleWithDailyBalance, SaleWithDailyBalanceAdmin)

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'

@admin.register(SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    date_hierarchy = 'date_sale'
    list_filter = ('date_sale',)
    search_fields = ('date_sale',)
    actions = None
    # Prevent additional queries for pagination.
    show_full_result_count = False
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)


        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            # See issue #172.
            # When an invalid filter is used django will redirect. In this
            # case the response is an http redirect response and so it has
            # no context_data.
            return response

        # List view

        metrics = {
            'total': Count('id'),
            'total_sales': Sum('value'),
        }

        response.context_data['summary'] = list(
            qs
            .values('date_sale')
            .annotate(**metrics)
            .order_by('-total_sales')
        )

        # List view summary
        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period
        summary_over_time = qs.annotate(
            period=Trunc('created', 'day', output_field=DateTimeField()),
        ).values('period').annotate(total=Sum('value')).order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
               ((x['total'] or 0) - low) / (high - low) * 100
               if high > low else 0,
        } for x in summary_over_time]

        return response
