from django.contrib import admin

from .models import Bank, CardEntity, CreditCard, DebitCard, Card
# Register your models here.

#admin.site.register(Card)
#admin.site.register(DebitCard)
#admin.site.register(CreditCard)

class BankAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Bank, BankAdmin)

class CardEntityAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(CardEntity, CardEntityAdmin)

class CardAdmin(admin.ModelAdmin):
    fields = ('card_entity', 'bank')
    list_select_related = ('card_entity', 'bank')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Card, CardAdmin)

class DebitCardAdmin(admin.ModelAdmin):
    fields = ('card_entity', 'bank')
    list_select_related = ('card_entity', 'bank')

admin.site.register(DebitCard, DebitCardAdmin)

class CreditCardAdmin(admin.ModelAdmin):
    fields = ('card_entity', 'bank')
    list_select_related = ('card_entity', 'bank')

admin.site.register(CreditCard, CreditCardAdmin)
