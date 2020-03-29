from django.db import models

from django.db.models import Sum, F, FloatField
from django.utils import timezone
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from utils.models_mixin import StatusCreatedUpdatedModelMixin
# Create your models here.

class Overhead(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a overhead."""

    #init_cash = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name="Caja inicial")
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name="Total gastos")
    #remaining_cash = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name="Efectivo restante")
    date_overhead = models.DateField(default=timezone.now, verbose_name="Fecha")

    class Meta:
        ordering = ['-date_overhead']
        verbose_name = "gasto del día"
        verbose_name_plural = "gastos del día"

    def calculate_total(self):
        tot = self.itemoverhead_set.all().aggregate(
            tot_overhead=Sum( F('value'), output_field=FloatField() ) # Devuelve un diccionario con un dato cuya key es 'tot_sale' 
        )['tot_overhead'] or 0
        
        self.total = tot
        #remaining = float(self.init_cash) - self.total
        #self.remaining_cash = remaining
        
        #super(Overhead, self).save(update_fields=['total', 'remaining_cash'])
        #Overhead.objects.filter(id=self.id).update(total=tot, remaining_cash=remaining)
        Overhead.objects.filter(id=self.id).update(total=tot)

    def __str__(self):
        return 'GASTOS: {}'.format(self.date_overhead)

class ItemOverhead(models.Model):
    """Model representing a overhead."""

    name = models.CharField(max_length=50, default='Gastos', verbose_name="Nombre")
    value = models.DecimalField(default=0.0, max_digits=8, decimal_places=2, verbose_name="Valor")

    overhead = models.ForeignKey(Overhead, on_delete=models.CASCADE, verbose_name="Gasto")

    class Meta:
        ordering = ['id']
        verbose_name = "gasto"
        verbose_name_plural = "gastos"

    def delete(self, *args, **kwargs):
        overhead = self.overhead

        super(ItemOverhead, self).delete(*args, **kwargs)
        overhead.calculate_total()

    def __str__(self):
        return '{}'.format(self.name)

@receiver(post_save, sender=ItemOverhead)
def update_total_overheads_at_item(sender, instance, **kwargs):
    instance.overhead.calculate_total()

@receiver(post_save, sender=Overhead)
def update_overheads_total(sender, instance, **kwargs):
    instance.calculate_total()

@receiver(pre_delete, sender=ItemOverhead)
def update_total_overhead_delete_item(sender, instance, **kwargs):
    instance.overhead.calculate_total()