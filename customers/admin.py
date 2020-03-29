from django.contrib import admin

from .models import Customer
from persons.models import Address
# Register your models here.

class AddressAdmin(admin.TabularInline):
    model = Address
    autocomplete_fields = ('city',)
    fields = ('street', 'number_street', 'city', 'type_address')
    list_display = ('get_address', 'city')
    ordering = ('id',)
    list_editable = ('street', 'number_street', 'city', 'type_address')
    list_select_related = ('city',)
    extra = 1

    def get_address(self, obj):
        return obj.__str__()
    get_address.short_description = "Dirección"

class CustomerAdmin(admin.ModelAdmin):
    fields = ( ('id_card', 'last_name'), ('first_name', 'birth_date'), ('movile', 'telephone'), )
    readonly_fields = ('created', 'updated')
    list_display = ('full_name', 'movile')
    ordering = ('last_name', 'first_name', 'id_card')
    search_fields = ('id_card', 'last_name', 'first_name')
    date_hierarchy = 'updated' # Jerarquizar por fechas
    list_filter = ('last_name',)
    inlines = [AddressAdmin,]

admin.site.register(Customer, CustomerAdmin)