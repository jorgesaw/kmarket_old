# Generated by Django 2.2.1 on 2019-09-06 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20190905_2122'),
        ('locations', '0002_remove_address_city'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
    ]
