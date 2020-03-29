# Generated by Django 2.2.1 on 2019-09-06 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overheads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='overhead',
            name='init_cash',
        ),
        migrations.RemoveField(
            model_name='overhead',
            name='remaining_cash',
        ),
        migrations.AlterField(
            model_name='itemoverhead',
            name='name',
            field=models.CharField(default='Gastos', max_length=50, verbose_name='Nombre'),
        ),
    ]
