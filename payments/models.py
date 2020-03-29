from django.db import models

from sales.models import Sale
from utils.models_mixin import StatusCreatedUpdatedModelMixin 
# Create your models here.

class Bank(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a bank."""

    name = models.CharField(max_length=255, verbose_name="Nombre")

    class Meta:
        ordering = ['-name']
        verbose_name = "banco"
        verbose_name_plural = "banco"

    def __str__(self):
        return self.name

class CardEntity(StatusCreatedUpdatedModelMixin, models.Model):
    """"Model representing at Card Entity"""
    name = models.CharField(max_length=50, verbose_name="Tarjeta")
    
    class Meta:
        verbose_name = "entidad de tarjeta"
        verbose_name_plural = "entidad de tarjetas"
        
    def __str__(self):
        return self.name

class Card(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a apyment of cash."""

    name = models.CharField(max_length=25, verbose_name="Tipo")
    card_entity = models.ForeignKey(CardEntity, on_delete=models.CASCADE, verbose_name='Entidad')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='Banco')

    class Meta:
        verbose_name = "tarjeta"
        verbose_name_plural = "tarjetas"

    def save(self, *args, **kwargs):
        super(Card, self).save(*args, **kwargs)
        payment_card = CardPayment(card=self)
        payment_card.save()

    def __str__(self):
        return 'Tarjeta: {} {} {}'.format(self.name, self.card_entity, self.bank)

class CreditCard(Card):
    """Model representing a payment of card."""

    class Meta:
        verbose_name = "tarjeta de crédito"
        verbose_name_plural = "tarjeta de créditos"

    def save(self, *args, **kwargs):
        self.name = "CREDITO"
        super(CreditCard, self).save(*args, **kwargs)

        
    def __str__(self):
        return 'Tarjeta CREDITO - {}'.format(super(CreditCard, self).bank)

class DebitCard(Card):
    """Model representing a payment of card."""

    class Meta:
        verbose_name = "tarjeta de débito"
        verbose_name_plural = "tarjeta de débitos"

    def save(self, *args, **kwargs):
        self.name = "DEBITO"
        super(DebitCard, self).save(*args, **kwargs)
        
    def __str__(self):
        return 'Tarjeta DEBITO - {}'.format(super(DebitCard, self).bank)

class PaymentType(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a payment type."""
    
    class Meta:
        ordering = ['id']
        verbose_name = "forma de pago"
        verbose_name_plural = "forma de pagos"

    @property
    def display_subclass_str(self):
        for attr in ('cardpayment', 'cashpayment', 'currentpayment'):
            if hasattr(self, attr):
                return getattr(self, attr).__str__() # igual a self.cardpayment.__str__()
        return None

    def __str__(self):
        return self.display_subclass_str

PESOS_CURRENCY = '$ ARG'
DEFAULT_CURRENCY_CHOICE = PESOS_CURRENCY
CURRENCY_CHOICES = (
    (PESOS_CURRENCY, PESOS_CURRENCY),
)

class CashPayment(PaymentType):
    """Model representing a apyment of cash."""

    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default=DEFAULT_CURRENCY_CHOICE, verbose_name='Moneda')

    class Meta:
        verbose_name = "efectivo"
        verbose_name_plural = "efectivos"
        
    def __str__(self):
        return 'Efectivo: {}'.format(super(Cash, self).amount)

class CurrentPayment(PaymentType):
    """Model representing a current account."""

    paid_out = models.BooleanField(default=False, verbose_name='Cuenta Corriente')

    class Meta:
        verbose_name = "cuenta corriente"
        verbose_name_plural = "cuentas corrientes"
        
    def __str__(self):
        return 'Cuenta Corriente'

class CardPayment(PaymentType):
    """Model representing a current account."""

    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='Tarjeta')

    class Meta:
        verbose_name = "tarjeta"
        verbose_name_plural = "tarjetas"
        
    def __str__(self):
        return self.card.__str__()
        
class Payment(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a payment."""

    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, verbose_name="Importe")
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, verbose_name='Forma de pago')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta')

    class Meta:
        ordering = ['id']
        verbose_name = "pago"
        verbose_name_plural = "pagos"
