from django.db import models
from django.urls import reverse_lazy

from utils.models_mixin import StatusCreatedUpdatedModelMixin
# Create your models here.

class State(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a state."""
    name = models.CharField(max_length=210, help_text="Enter a article", verbose_name="Nombre")

    class Meta:
        ordering = ['name']
        verbose_name = "provincia"
        verbose_name_plural = "provincias"

    def get_absolute_url(self):
        """Returns the url to access a particular state instance."""
        return ""#reverse_lazy('article-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return '{}'.format(self.name)

class City(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a city."""
    
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    zip_city = models.CharField(max_length=30, null=True, blank=True, verbose_name="Código postal")
    ddn = models.CharField(max_length=12, null=True, blank=True, verbose_name="Característica")

    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, verbose_name='Provincia')

    class Meta:
        ordering = ['name']
        verbose_name = "ciudad"
        verbose_name_plural = "ciudades"

    def get_absolute_url(self):
        """Returns the url to access a particular city instance."""
        return ""#reverse_lazy('article-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return '{}'.format(self.name)
