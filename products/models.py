from django.db import models
from django.urls import reverse_lazy

from utils.models_mixin import StatusCreatedUpdatedModelMixin
# Create your models here.

class AbstractCategory(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a category of product."""
    name = models.CharField(max_length=150, verbose_name="Nombre")

    class Meta:
        abstract = True
        ordering = ['-created']
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def get_absolute_url(self):
        """Returns the url to access a particular category instance."""
        return ""#reverse_lazy('category-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.name

class Category(AbstractCategory):
    pass

class AbstractProductWithoutPrice(StatusCreatedUpdatedModelMixin, models.Model):
    """Model representing a product."""
    code = models.CharField(max_length=30, unique=True, verbose_name="Código")
    name = models.CharField(max_length=210, verbose_name="Nombre")
    desc = models.CharField(max_length=255, help_text="Enter adescription", verbose_name="Descripción")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    stock_min = models.PositiveIntegerField(default=0, verbose_name="Stock mínimo")
    stock_max = models.PositiveIntegerField(default=0, blank=True, verbose_name="Stock máximo")
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name="Imagen")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def get_absolute_url(self):
        """Returns the url to access a particular product instance."""
        return ""#reverse_lazy('product-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return '{}'.format(self.name)

class AbstractProduct(AbstractProductWithoutPrice):
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Precio")

class Product(AbstractProduct):
    pass

class ProductWithoutPrice(AbstractProductWithoutPrice):
    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"


class ProductProxi(ProductWithoutPrice):
    class Meta:
        proxy = True
        verbose_name_plural = "Stocks"
        
class Price(models.Model):
    """Model representing a price."""
    value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Valor")

    class Meta:
        ordering = ['id']
        verbose_name = "precio"
        verbose_name_plural = "precios"

    def get_absolute_url(self):
        """Returns the url to access a particular product instance."""
        return ""#reverse_lazy('product-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return '{}'.format(self.value)


class PriceWithDesc(Price):
    """Model representing a price."""
    desc = models.CharField(max_length=210, verbose_name="Tipo de precio")

    product = models.ForeignKey(ProductWithoutPrice, on_delete=models.CASCADE)

    class Meta:
        ordering = ['desc']
        verbose_name = 'precio con descripcion'
        verbose_name_plural = 'precios con descripcion'

    def __str__(self):
        return '{} ({}) - $ {}'.format(self.product.name, self.desc, self.value)
