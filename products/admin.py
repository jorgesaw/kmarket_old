from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Product, Category, ProductWithoutPrice, PriceWithDesc, ProductProxi

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
    readonly_fields = ('created', 'updated')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class PriceAdmin(admin.ModelAdmin):
    #fields = ('desc', 'value')
    list_display = ('desc', 'value', 'product')
    ordering = ('id',)
    search_fields = ('desc', )
    extra = 1

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

admin.site.register(PriceWithDesc, PriceAdmin)

class PriceTabularAdmin(admin.TabularInline):
    model = PriceWithDesc
    fields = ('desc', 'value')
    list_display = ('desc', 'value')
    ordering = ('id',)
    search_fields = ('desc', )
    extra = 1

"""
from django import forms
class PriceForm(forms.ModelForm):
    hola = forms.CharField()
    
    class Meta:
        ProductWithoutPrice
"""

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('active', 'code', 'name', 'category', 'stock'),
        }),
    )
    autocomplete_fields = ('category',)
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'code', 'category_view')
    ordering = ('name', 'code')
    search_fields = ('code', 'name', 'desc', 'category__name')
    date_hierarchy = 'updated' # Jerarquizar por fechas
    list_filter = ('category__name', )
    #form = PriceForm
    #inlines = [PriceTabularAdmin,]

    """
    def save_model(self, request, obj, form, change):
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        print(form.cleaned_data.get('hola', None))
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        super().save_model(request, obj, form, change)
    """

    def category_view(self, obj):
        link = reverse("admin:products_category_change", args=[obj.category.id])
        return format_html('<a href="{}">Editar {}</a>', link, obj.category.name)
    category_view.short_description = "Categoría"

admin.site.register(Product, ProductAdmin)

from django import forms
class StockForm(forms.ModelForm):
    nueva_cant = forms.IntegerField()
    
    class Meta:
        ProductWithoutPrice

class ProductStockAdmin(ProductAdmin):
    form = StockForm
    readonly_fields = ('name', 'stock',)
    fieldsets = (
        (None, {
            'fields': ('name', 'stock', 'nueva_cant'),
        }),
    )
    list_display = ('name', 'stock')
    search_fields = ('name', 'code', 'category__name')
    list_filter = ('category__name', )
    inlines = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True
    
    def save_model(self, request, obj, form, change):
        nueva_cant = form.cleaned_data.get('nueva_cant', None)
        if obj.stock:
            obj.stock += nueva_cant
        else:
            obj.stock = nueva_cant
        super().save_model(request, obj, form, change)


admin.site.register(ProductProxi, ProductStockAdmin)
