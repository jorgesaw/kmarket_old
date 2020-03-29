from django.db import models
from django.utils import timezone

from utils.models_mixin import StatusCreatedUpdatedModelMixin
# Create your models here.

class DailyBalance(StatusCreatedUpdatedModelMixin, models.Model):
    """Model at representing a balance of day"""

    date_balance = models.DateField(default=timezone.now, verbose_name="Fecha")
    init_cash = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name="Caja inicial")
    total = 0.0

    class Meta:
        ordering = ['-date_balance']
        verbose_name = "saldo diario"
        verbose_name_plural = "saldos diarios"

    def __str__(self):
        return 'SALDO: {}'.format(self.date_balance)
