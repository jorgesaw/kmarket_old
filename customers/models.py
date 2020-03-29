from django.db import models

from persons.models import Person

# Create your models here.

class Customer(Person):
    """Model representing a customer."""

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"