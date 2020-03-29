from django.db import models
from django.db.models import Max, Avg, Min, Count


class SaleManager(models.Manager):
    def media(self):
        return self.all().aggregate(Avg('value'))['value__avg']

    def media_descoints(self):
        return self.all().aggregate(Avg('desconto'))['desconto__avg']

    def min(self):
        return self.all().aggregate(Min('value'))['value__min']

    def max(self):
        return self.all().aggregate(Max('value'))['value__max']

    def count_sales(self):
        return self.all().aggregate(Count('id'))['id__count']

    def count_sales_fiscal_bill(self):
        return self.filter(fiscal_bill=True).aggregate(Count('id'))['id__count']