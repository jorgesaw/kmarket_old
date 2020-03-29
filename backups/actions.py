

def load_restore_data(model_admin, request, queryset):
    if queryset.count() > 0:
        obj = queryset[0]
        return obj.provider_bck.restore_bck()
    return False

load_restore_data.short_description = 'Restaurar datos'
