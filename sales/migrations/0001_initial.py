# Generated by Django 2.2.1 on 2019-09-05 23:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0, help_text='Ingresa la cantidad', verbose_name='Cantidad')),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ItemSaleWithPrice',
            fields=[
                ('itemsale_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.ItemSale')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
            bases=('sales.itemsale',),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('number_sale', models.CharField(help_text='Ingresar N°', max_length=18, verbose_name='Número')),
                ('date_sale', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('fiscal_bill', models.BooleanField(default=True, help_text='Es fiscal', verbose_name='AFIP')),
                ('tax', models.CharField(choices=[('0', 0.0), ('1', 0.21), ('2', 0.105)], default='0', max_length=2, verbose_name='IVA')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.Customer')),
            ],
            options={
                'verbose_name': 'venta',
                'verbose_name_plural': 'ventas',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='itemsale',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale', verbose_name='Venta'),
        ),
        migrations.CreateModel(
            name='SaleSummary',
            fields=[
            ],
            options={
                'verbose_name': 'reporte venta',
                'verbose_name_plural': 'reporte de ventas',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sales.sale',),
        ),
    ]
