from django.contrib import admin
from django.contrib import messages

from backups import models
from .models import BackUp
from .actions import load_restore_data
# Register your models here.

class BackUpAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ( 'created', 'desc' )
        }),
    )
    readonly_fields = ('created',)
    list_display = ('created', 'desc')
    ordering = ('-created',)
    search_fields = ('created',)
    date_hierarchy = 'created' # Jerarquizar por fechas
    list_filter = ('created', )
    actions = ['load_restore_data',]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def load_restore_data(self, request, queryset):
        level = messages.INFO
        msg = models.MSG_RESTORE_DATA_DONE

        if queryset.count() > 1:
            msg = "Necesita seleccionar sólo un dato para restaurar."
            level=messages.WARNING
        elif not load_restore_data(self, request, queryset):
            msg = models.MSG_RESTORE_DATA_ERROR
            level=messages.ERROR

        return self.message_user(request, msg, level)
    load_restore_data.short_description = "Restaurar datos"

admin.site.register(BackUp, BackUpAdmin)
