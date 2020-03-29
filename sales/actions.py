

def fiscal_bill_emited(model_admin, request, queryset):
    queryset.update(fiscal_bill=True)

fiscal_bill_emited.short_description = 'Nota fiscal emitida'

def fiscal_bill_not_emited(model_admin, request, queryset):
    queryset.update(fiscal_bill=False)

fiscal_bill_not_emited.short_description = 'Nota fiscal sin emitir'