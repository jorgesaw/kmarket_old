from django.db import models
from django.db import transaction
from django.contrib.auth.models import User

from utils.models_mixin import StatusCreatedUpdatedModelMixin
from locations.models import City
# Create your models here.

class AbstractPerson(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a person."""

    id_card = models.CharField(max_length=30, unique=True, verbose_name="DNI")
    first_name = models.CharField(max_length=210, verbose_name="Nombre")
    last_name = models.CharField(max_length=210, verbose_name="Apellido")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    desc = models.TextField(null=True, blank=True, verbose_name="Descripción")

    movile = models.CharField(max_length=50, null=True, blank=True, verbose_name="Celular")
    telephone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Teléfono")

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        abstract = True
        ordering = ['last_name']
        verbose_name = "persona"
        verbose_name_plural = "personas"

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.full_name

class Person(AbstractPerson):
    """Model representing a person with addresses."""
    pass

DEFAULT_TYPE_ADDRESS = "Residence"
TYPE_ADDRESS_CHOICES = (
    (DEFAULT_TYPE_ADDRESS, DEFAULT_TYPE_ADDRESS), 
)

class Address(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a address."""
    
    street = models.CharField(max_length=50, verbose_name='Calle')
    number_street = models.CharField(max_length=18, verbose_name='Número')
    floor = models.CharField(max_length=18, null=True, blank=True, verbose_name='Piso')
    departament = models.CharField(max_length=18, null=True, blank=True, verbose_name='Departamento')

    type_address = models.CharField(max_length=12, choices=TYPE_ADDRESS_CHOICES, default=DEFAULT_TYPE_ADDRESS, verbose_name='Tipo de residencia')

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Ciudad')
    person = models.ForeignKey(Person, on_delete=models.CASCADE,  verbose_name='persona')

    class Meta:
        ordering = ['street', 'number_street']
        verbose_name = "dirección"
        verbose_name_plural = "direcciones"

    def get_absolute_url(self):
        """Returns the url to access a particular city instance."""
        return ""#reverse_lazy('article-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return '{} {}'.format(self.street, self.number_street)

class AbstractPersonUser(AbstractPerson):
    """Model representing a person with user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    @transaction.atomic
    def save(self, *args, **kwargs):
        user = User(username=self.id_card)
        user.set_password(self.id_card)
        user.save()
        self.user = user
        super(AbstractPerson, self).save(*args, **kwargs)
